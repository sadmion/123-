#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""源码还原校验器 —— 比对「还原出的源码」与「原始字节码」是否语义一致。

原理
----
把还原出的 .py 编译成字节码，与原始 .pyc 里对应的函数逐个比对：
  · 函数清单比对    —— 有没有漏函数 / 多函数
  · 关键常量比对    —— 字符串、数字字面量是否一致（最容易出错的地方）
  · 变量名比对      —— 局部变量、参数名是否一致
  · 属性名比对      —— 调用了哪些方法 / 属性
  · 控制流骨架比对  —— 跳转指令的数量与种类分布

用途
----
还原完一个模块后，立刻跑一次，把「还原过程中猜错/漏写」的地方抓出来。
这类错误（如 return 写成 break、漏掉翻页）不会导致语法错误，
但会让程序行为不对，必须靠机械比对发现。

用法
----
    python tools/verify_src.py pan123_api
    python tools/verify_src.py pan123_api --detail      # 打印差异明细
    python tools/verify_src.py --all
"""
import argparse
import collections
import dis
import marshal
import os
import sys
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BYTECODE_DIR = os.path.join(ROOT, 'tools', 'bytecode')
SRC_DIR = os.path.join(ROOT, 'src')


def load_bytecode_code(name):
    """读取原始 .pyc 的顶层 code 对象。"""
    p = os.path.join(BYTECODE_DIR, name + '.pyc')
    if not os.path.isfile(p):
        raise FileNotFoundError(p)
    return marshal.loads(open(p, 'rb').read()[16:])


def compile_src(name):
    """把还原出的源码编译成 code 对象。"""
    p = os.path.join(SRC_DIR, name + '.py')
    if not os.path.isfile(p):
        raise FileNotFoundError(p)
    src = open(p, encoding='utf-8').read()
    return compile(src, p, 'exec')


def walk_codes(code, out=None):
    out = [] if out is None else out
    out.append(code)
    for k in code.co_consts:
        if isinstance(k, types.CodeType):
            walk_codes(k, out)
    return out


def ins_list(code):
    """取指令序列（过滤掉与源码写法无关的伪指令）。"""
    skip = {'RESUME', 'CACHE', 'NOP', 'PRECALL', 'EXTENDED_ARG',
            'MAKE_CELL', 'COPY_FREE_VARS', 'RETURN_GENERATOR'}
    out = []
    for i in dis.get_instructions(code):
        if i.opname in skip:
            continue
        out.append(i)
    return out


def sig(code):
    """函数的可比对特征。"""
    literals = []
    for k in code.co_consts:
        if isinstance(k, (str, int, float, bytes)) or k is None or k is True or k is False:
            literals.append(k)
    ops = collections.Counter(i.opname for i in ins_list(code))
    jumps = collections.Counter(
        i.opname for i in ins_list(code)
        if i.opname.startswith(('POP_JUMP', 'JUMP', 'FOR_ITER')))
    return {
        'argcount': code.co_argcount,
        'varnames': tuple(code.co_varnames),
        'names': tuple(sorted(set(code.co_names) - _CLS_INJECTED)),
        'literals': tuple(sorted(map(repr, literals))),
        'n_ins': sum(ops.values()),
        'ops': ops,
        'jumps': jumps,
        'ncells': len(code.co_cellvars) + len(code.co_freevars),
    }


# 类体自动生成的属性名，与源码无关
_CLS_INJECTED = {'__module__', '__qualname__', '__firstlineno__',
                 '__static_attributes__'}

# Python 3.12+ 零参 super() 会把所在类名编进 co_names。
# 两边类名一致，只是出现位置不同，比对时统一剔除。
_KNOWN_CLASSES = {'TaskState', 'ExtractTask', 'ImportTask',
                  'Library', 'LibraryStore', 'Work', 'Handler'}


def collect_funcs(code):
    """收集 {限定名: code}，跳过 <module> / 推导式等匿名对象。"""
    res = {}

    def rec(c, prefix):
        for k in c.co_consts:
            if not isinstance(k, types.CodeType):
                continue
            nm = k.co_name
            if nm.startswith('<'):
                # lambda / 推导式 / genexpr 也纳入，但用序号区分
                if nm == '<lambda>':
                    res[prefix + '<lambda>@%d' % k.co_firstlineno] = k
                rec(k, prefix)
                continue
            key = prefix + nm
            res[key] = k
            rec(k, key + '.')
    rec(code, '')
    return res


def cmp_one(ref, got, name, detail):
    """比对单个函数，返回问题列表。"""
    problems = []
    a, b = sig(ref), sig(got)

    if a['argcount'] != b['argcount']:
        problems.append('参数个数 %d → %d' % (a['argcount'], b['argcount']))

    # 字面量：最关键的比对项。
    # 类体（co_name 是类名，且含 __qualname__）会带 firstlineno 数字常量，
    # 该值与源码行号绑定，无法也不需要对上，做过滤。
    # 类体会带 firstlineno（如 28），它等于文件行号，受注释与空行影响。
    # 行号不构成语义问题，两边都剔除 100 以上的整数字面量再比对。
    # 类体的 __firstlineno__ 常量就是文件行号。这里先从待比对集合里
    # 精确剔除「类体存的那个行号值」，不会误伤源码里的真实小整数。
    def drop_firstlineno(code, items):
        if '__firstlineno__' not in code.co_names:
            return items
        # 类体里 __firstlineno__ 紧跟在 __qualname__ 之后，按常量表顺序找
        vals = [k for k in code.co_consts if isinstance(k, int)]
        if len(vals) == 1:
            items = {x for x in items if x != repr(vals[0])}
        return items

    la = drop_firstlineno(ref, set(a['literals']))
    lb = drop_firstlineno(got, set(b['literals']))
    missing = sorted(la - lb)
    extra = sorted(lb - la)
    if missing:
        problems.append('缺少字面量 %d 个: %s' % (
            len(missing), ', '.join(x[:40] for x in missing[:4])))
    if extra:
        problems.append('多出字面量 %d 个: %s' % (
            len(extra), ', '.join(x[:40] for x in extra[:4])))

    # 变量名
    va, vb = set(a['varnames']), set(b['varnames'])
    if va - vb:
        problems.append('缺少变量: %s' % ', '.join(sorted(va - vb)[:5]))
    if vb - va:
        problems.append('多出变量: %s' % ', '.join(sorted(vb - va)[:5]))

    # 属性/方法名
    # Python 3.12+ 的零参 super() 会把「所在类名」编进 co_names，
    # 属编译器行为差异而非语义问题，先剔除这些类名再比对。
    na = set(a['names']) - _KNOWN_CLASSES
    nb = set(b['names']) - _KNOWN_CLASSES
    if na - nb:
        problems.append('缺少名字: %s' % ', '.join(sorted(na - nb)[:6]))
    if nb - na:
        problems.append('多出名字: %s' % ', '.join(sorted(nb - na)[:6]))

    # 控制流骨架：跳转指令分布。
    # 注意：and/or/三元/嵌套 if 的写法差异都会改变跳转分布，
    # 但语义可能等价。因此仅在「分支总数差异较大」时判为问题，
    # 细微差异（±1）降级为提示。
    ja, jb = a['jumps'], b['jumps']
    if ja != jb:
        ta, tb = sum(ja.values()), sum(jb.values())
        if abs(ta - tb) > 1:
            problems.append('分支数不同: 原 %d 个 / 新 %d 个  %s  vs  %s'
                            % (ta, tb, dict(ja), dict(jb)))
        else:
            problems.append('(提示) 跳转写法略有差异，语义可能等价: %s vs %s'
                            % (dict(ja), dict(jb)))

    # 指令规模（超出 ±25% 视为结构差异较大）
    if a['n_ins'] and abs(a['n_ins'] - b['n_ins']) / a['n_ins'] > 0.25:
        problems.append('指令数 %.0f → %.0f（差 %.0f%%）' % (
            a['n_ins'], b['n_ins'],
            (b['n_ins'] - a['n_ins']) / a['n_ins'] * 100))

    if b['ncells'] and not a['ncells']:
        problems.append('闭包结构丢失（原 %d 个 cell，新 0 个）' % b['ncells'])

    return problems


def verify(name, detail=False):
    print('=' * 68)
    print('模块: %s' % name)
    print('=' * 68)

    ref_code = load_bytecode_code(name)
    try:
        got_code = compile_src(name)
    except SyntaxError as e:
        print('  ✗ 语法错误 第 %s 行: %s' % (e.lineno, e.msg))
        return 1
    except Exception as e:
        print('  ✗ 无法编译: %s: %s' % (type(e).__name__, e))
        return 1

    ref = collect_funcs(ref_code)
    got = collect_funcs(got_code)

    only_ref = sorted(set(ref) - set(got))
    only_got = sorted(set(got) - set(ref))
    both = sorted(set(ref) & set(got))

    print('  函数数: 原始 %d 个 / 还原 %d 个 / 可比对 %d 个'
          % (len(ref), len(got), len(both)))
    print()

    if only_ref:
        print('  ✗ 漏掉的函数 (%d):' % len(only_ref))
        for f in only_ref:
            print('      %s' % f)
        print()
    if only_got:
        print('  ! 新增的函数 (%d):' % len(only_got))
        for f in only_got:
            print('      %s' % f)
        print()

    ok = bad = 0
    details = []
    for f in both:
        p = cmp_one(ref[f], got[f], f, detail)
        # 「提示」类不算失败（写法差异但语义等价）
        real = [x for x in p if not x.startswith('(提示)')]
        if real:
            bad += 1
            details.append((f, p))
        else:
            ok += 1

    print('  逐函数比对: 一致 %d / 有差异 %d' % (ok, bad))
    if details:
        print()
        for f, p in details:
            print('  · %s' % f)
            for x in p:
                print('        - %s' % x)

    print()
    score = ok * 100 // max(len(both), 1)
    verdict = ('通过' if score >= 95 and not only_ref
               else '需继续修' if score >= 60
               else '差异较大')
    print('  一致率: %d%%  →  %s' % (score, verdict))
    return 0 if (score >= 95 and not only_ref) else 1


def main():
    ap = argparse.ArgumentParser(description='源码还原校验器')
    ap.add_argument('module', nargs='?', help='模块名，如 pan123_api')
    ap.add_argument('--all', action='store_true', help='校验全部模块')
    ap.add_argument('--detail', action='store_true', help='打印差异明细')
    a = ap.parse_args()

    names = ['pan123_api', 'tasks', 'library_store', 'server'] if a.all else [a.module]
    if not names or names == [None]:
        ap.print_help()
        return 2

    rc = 0
    for n in names:
        if not os.path.isfile(os.path.join(SRC_DIR, n + '.py')):
            print('=' * 68)
            print('模块: %s  →  src/%s.py 尚不存在，跳过' % (n, n))
            rc = 1
            continue
        rc |= verify(n, a.detail)
        print()
    return rc


if __name__ == '__main__':
    sys.exit(main())
