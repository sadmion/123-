#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_src.py —— 结构化反编译主程序（CPython 3.13）

把 cf_313 的块级结构分析与表达式栈还原结合起来，产出源码。

核心算法（结构化的关键）：
  对每个代码对象，模拟"结构化遍历"：
    - 遇到 for/while 头块 -> 输出 for/while，递归处理循环体
    - 遇到条件跳转 + 前向跳转 -> 输出 if / if-else
    - 遇到异常表覆盖的区间 -> 输出 try / except
    - 其余块顺序输出语句

  为控制复杂度并保证正确性，这里采用"递归下降 + 区间处理"：
  每条语句由一小段指令生成，缩进由所在结构决定。

用法:
    python build_src.py <pyc目录> <输出目录>
"""
import dis
import marshal
import os
import sys
import types

sys.setrecursionlimit(20000)      # 大函数 + 深表达式需要更大的递归预算

# 复用表达式还原能力
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decompiler_313 import Frame, render_func, render_class, Bail  # noqa

# dis.get_instructions / _parse_exception_table 在超大函数上开销大，做缓存
_INSN_CACHE = {}
_TRY_CACHE = {}
_RENDERED = set()        # 已渲染过的嵌套代码对象 id，防重复展开


try:
    from dis import _unpack_opargs as _raw_opargs
except ImportError:      # 版本差异兜底
    _raw_opargs = None


class _Ins:
    """轻量指令对象，替代 dis.Instruction，避免其内部递归构建标签表。"""
    __slots__ = ("opname", "opcode", "arg", "argval", "offset", "argrepr")

    def __init__(self, opname, opcode, arg, argval, offset, argrepr=""):
        self.opname = opname
        self.opcode = opcode
        self.arg = arg
        self.argval = argval
        self.offset = offset
        self.argrepr = argrepr

    def __repr__(self):
        return "<%s %r @%d>" % (self.opname, self.argval, self.offset)


SKIP_OPS = {"RESUME", "CACHE", "NOP", "PRECALL", "EXTENDED_ARG"}


def clean_ins(code):
    """线性解析指令，避开 dis.get_instructions 的递归标签表构建。

    大函数（如 1860 条指令）会让 dis 内部 findlabels 触发 RecursionError，
    这里直接用 _unpack_opargs + opname/opmap 自行组装，完全不递归。
    """
    key = id(code)
    if key in _INSN_CACHE:
        return _INSN_CACHE[key]

    import opcode as _op
    opname = _op.opname
    HAVE = _op.HAVE_ARGUMENT
    result = []
    if _raw_opargs is not None:
        for row in _raw_opargs(code.co_code):
            # 不同小版本返回 3 或 4 元组（3.13 起含 start_offset）
            if len(row) == 4:
                _start, offset, op, arg = row
            else:
                offset, op, arg = row
            if arg is not None:
                argval = arg
                nm = opname[op]
                # 解析参数语义（常量 / 变量名 / 跳转目标）。
                # 用 try 包裹：3.13 的部分指令（如 LOAD_GLOBAL 带 flag 位）
                # 会让朴素判断越界，越界时退回原始 arg 而不是崩溃。
                try:
                    if op in _op.hasconst:
                        argval = code.co_consts[arg]
                    elif op in _op.hasfree:
                        # ⚠️ 3.13 的 DEREF 类指令（含 MAKE_CELL）使用**统一索引空间**：
                        # arg 先指向 co_varnames 段，超出后才落到 cellvars/freevars。
                        # 实测：load_auth 的 co_cellvars=('t',) 而 MAKE_CELL arg=3，
                        # 对应 ('f','d','_verify','t')[3]。只查 cellvars 会取不到。
                        nv = len(code.co_varnames)
                        if arg < nv:
                            argval = code.co_varnames[arg]
                        else:
                            names = (code.co_cellvars + code.co_freevars)
                            k2 = arg - nv
                            argval = names[k2] if 0 <= k2 < len(names) else arg
                    elif op in _op.haslocal:
                        argval = code.co_varnames[arg]
                    elif op in _op.hasname:
                        # LOAD_GLOBAL / LOAD_ATTR 在 3.11+ 的 arg 低位带 flag
                        idx = (arg >> 1) if nm in ("LOAD_GLOBAL", "LOAD_ATTR",
                                                   "LOAD_METHOD",
                                                   "STORE_GLOBAL") else arg
                        argval = (code.co_names[idx]
                                  if 0 <= idx < len(code.co_names) else arg)
                    elif op in _op.hascompare:
                        argval = __import__("dis").cmp_op[arg]
                    elif op in _op.hasjrel or op in _op.hasjabs:
                        argval = (offset + 2 + arg) if op in _op.hasjrel else arg
                except Exception:
                    argval = arg
            else:
                argval = None
            nm = opname[op]
            if nm in SKIP_OPS:
                continue
            result.append(_Ins(nm, op, arg, argval, offset))
    _INSN_CACHE[key] = result
    return result


def _parse_varint(iterator):
    """3.13 异常表的 varint 解码（与 dis 内部一致）。"""
    b = next(iterator)
    val = b & 63
    while b & 64:
        val <<= 6
        b = next(iterator)
        val |= b & 63
    return val


def parse_try(code):
    """独立解析 co_exceptiontable，并区分「真正的 try/except」与「with 清理」。

    不调用 dis._parse_exception_table —— 后者内部会构建标签映射并递归，
    在本项目的大函数（1800+ 条指令）上会触发 RecursionError。
    这里用纯 varint 解码，零递归。

    返回条目列表：(start, end, target, depth, kind)
      kind="except"  target 处是 CHECK_EXC_MATCH，即真正的 except 处理
      kind="cleanup" 其余（with 的 __exit__ 清理、re-raise 等），不应还原成 try
    """
    key = id(code)
    if key in _TRY_CACHE:
        return _TRY_CACHE[key]

    raw = []
    try:
        it = iter(code.co_exceptiontable)
        while True:
            start = _parse_varint(it) * 2
            length = _parse_varint(it) * 2
            target = _parse_varint(it) * 2
            dl = _parse_varint(it)
            raw.append((start, start + length, target, dl >> 1))
    except StopIteration:
        pass
    except Exception:
        raw = []

    # 建立 偏移 -> 指令 的映射，用于判断 handler 是否为 except
    try:
        ins_map = {i.offset: i.opname for i in clean_ins(code)}
    except Exception:
        ins_map = {}

    def kind_of(target):
        """handler 首指令是 PUSH_EXC_INFO，紧跟着若出现 CHECK_EXC_MATCH
        即为显式 except X；否则是 with 清理或裸 re-raise。"""
        seq = []
        for off in sorted(ins_map):
            if off >= target:
                seq.append(ins_map[off])
            if len(seq) >= 6:
                break
        return "except" if "CHECK_EXC_MATCH" in seq else "cleanup"

    r = [(s, e, t, d, kind_of(t)) for (s, e, t, d) in raw]
    _TRY_CACHE[key] = r
    return r


class StructGen:
    """按结构生成源码行。"""

    def __init__(self, code, indent=0):
        self.code = code
        self.indent = indent
        self.ins = clean_ins(code)
        self.off2idx = {x.offset: k for k, x in enumerate(self.ins)}
        self.frame = Frame(code, indent=indent)
        self.lines = []
        self.handled = set()      # 已处理过的指令偏移
        self.func_defs = {}       # 嵌套代码对象 -> 名字（由 MAKE_FUNCTION 记录）
        self.trys = parse_try(code)
        self.consumed_try = set()  # 已生成过 try 的入口偏移（防重复递归）

    # ---------------------------------------------------------- 输出
    def out(self, s, lv=None):
        self.lines.append("\t" * (self.indent if lv is None else lv) + s)

    def blank(self):
        self.lines.append("")

    # ---------------------------------------------------------- 表达式
    def exec_one(self, ins, lv=None):
        """执行单条指令到表达式栈，并把产生的语句写入输出。"""
        f = self.frame
        f.indent = self.indent if lv is None else lv
        before = len(f.lines)
        fn = getattr(f, "i_" + ins.opname, None)
        try:
            if fn:
                fn(ins)
            else:
                f.fallback(ins)
        except Bail:
            raise
        except Exception as e:
            f.fallback(ins)
        # 把新产生的语句搬过来
        while len(f.lines) > before:
            self.lines.append(f.lines.pop(before))

    def eval_until(self, lo, hi, lv=None):
        """执行 [lo, hi) 区间的指令，只求值不输出语句（用于条件表达式）。"""
        for k in range(lo, hi):
            self.exec_one(self.ins[k], lv)

    # ---------------------------------------------------------- with
    def gen_nested_def(self, k, hi):
        """函数体/类体内的嵌套 def（含闭包）。

        模式：LOAD_CONST <CODE> | MAKE_FUNCTION | [SET_FUNCTION_ATTRIBUTE n] | STORE_*
        闭包情形前面还会有 LOAD_CLOSURE/BUILD_TUPLE 压入 cell 元组，
        这里统一按「忽略闭包样板，直接生成 def」处理（语义等价）。
        """
        code_obj = self.ins[k].argval
        j = k + 1
        while j < hi and self.ins[j].opname in (
                "MAKE_FUNCTION", "SET_FUNCTION_ATTRIBUTE", "COPY"):
            j += 1
        if j >= hi or self.ins[j].opname not in ("STORE_FAST", "STORE_NAME",
                                                 "STORE_DEREF", "STORE_GLOBAL"):
            return k          # 不是定义语句（可能是 lambda 等），交回常规流程
        fname = self.ins[j].argval or code_obj.co_name
        # 防重复：同一代码对象只渲染一次（嵌套层级里可能被多次看到）
        key = id(code_obj)
        if key in _RENDERED:
            for x in range(k, j + 1):
                self.handled.add(self.ins[x].offset)
            return j + 1
        _RENDERED.add(key)
        for line in render_func_struct(fname, code_obj, indent=self.indent):
            self.lines.append(line)
        self.lines.append("")
        for x in range(k, j + 1):
            self.handled.add(self.ins[x].offset)
        return j + 1

    def near_with(self, k, span=14):
        """向后探查：本语句是否是 with 的起点。

        判据：在碰到「会终结表达式」的指令前出现 BEFORE_WITH。
        """
        for j in range(k, min(k + span, len(self.ins))):
            nm = self.ins[j].opname
            if nm in ("BEFORE_WITH", "BEFORE_ASYNC_WITH"):
                return True
            if nm in ("STORE_FAST", "STORE_NAME", "POP_TOP", "RETURN_VALUE",
                      "RETURN_CONST", "FOR_ITER", "STORE_ATTR",
                      "STORE_SUBSCR", "STORE_DEREF"):
                return False
        return False

    def gen_with(self, k, hi):
        """还原 with 语句。

        3.13 的 with 结构：
            <ctx 表达式>
            BEFORE_WITH          # 建立上下文
            STORE_FAST var       # 可选：with ... as var
            ...body...
            <清理指令>
        """
        ins = self.ins[k]
        # 先把 ctx 表达式完整求值（执行到 BEFORE_WITH 为止），再取栈顶。
        # 注意顺序：不能在求值前 pop，否则取到的是上层遗留值。
        j = k
        while j < hi and self.ins[j].opname not in (
                "BEFORE_WITH", "BEFORE_ASYNC_WITH"):
            self.exec_one(self.ins[j])
            j += 1
        if j >= hi:
            return k + 1
        ctx = self.frame.pop()
        self.handled.add(self.ins[j].offset)
        jj = j + 1
        var = None
        if jj < len(self.ins) and self.ins[jj].opname in ("STORE_FAST",
                                                          "STORE_NAME"):
            var = self.ins[jj].argval
            self.handled.add(self.ins[jj].offset)
            jj += 1
        head = "with %s" % ctx
        if var:
            head += " as %s" % var
        self.out(head + ":")
        # with 体：到作用域结束
        body_hi = hi
        off_now = self.ins[jj].offset if jj < len(self.ins) else None
        for s, e, t, d, kind in self.trys:
            if off_now is not None and s <= off_now < e:
                body_hi = min(body_hi, self.idx_of(e, hi))
        body = self.sub(self.indent + 1)
        body.run(jj, body_hi)
        self.adopt(body)
        for x in range(k, body_hi):
            self.handled.add(self.ins[x].offset)
        return body_hi

    def idx_of(self, offset, hi):
        for j in range(hi):
            if self.ins[j].offset == offset:
                return j
        return hi

    # ---------------------------------------------------------- 主流程
    def run(self, lo=0, hi=None):
        hi = len(self.ins) if hi is None else hi
        # 深度保护：嵌套过深时退化为平铺，避免缩进爆炸
        too_deep = self.indent >= self.MAX_INDENT
        k = lo
        while k < hi:
            ins = self.ins[k]
            if ins.offset in self.handled:
                k += 1
                continue

            if too_deep:
                # 只还原表达式与简单语句，不再拆分控制流结构
                if ins.opname.startswith(("POP_JUMP", "JUMP")) or \
                        ins.opname == "FOR_ITER":
                    self.handled.add(ins.offset)
                    k += 1
                    continue
                self.exec_one(ins)
                k += 1
                continue

            # ---- for 循环：FOR_ITER 出现在当前位置
            if ins.opname == "FOR_ITER":
                nk = self.gen_for(k, hi)
                if nk > k:
                    k = nk
                    continue

            # ---- 嵌套 def / lambda：LOAD_CONST <code> | MAKE_FUNCTION | STORE
            if (ins.opname == "LOAD_CONST"
                    and isinstance(ins.argval, types.CodeType)):
                nk = self.gen_nested_def(k, hi)
                if nk > k:
                    k = nk
                    continue

            # ---- with 语句：向后探查若干条指令内是否出现 BEFORE_WITH
            if self.near_with(k):
                nk = self.gen_with(k, hi)
                if nk > k:
                    k = nk
                    continue

            # ---- try 作用域入口
            if self.is_try_entry(k):
                nk = self.gen_try(k, hi)
                if nk > k:
                    k = nk
                    continue

            # ---- 条件分支：POP_JUMP_IF_*
            if ins.opname.startswith("POP_JUMP"):
                nk = self.gen_if(k, hi)
                if nk > k:
                    k = nk
                    continue

            # ---- 普通语句
            self.exec_one(ins)
            k += 1
        return self.lines

    # ---------------------------------------------------------- try 判定
    def is_try_entry(self, k):
        """只把「真正的 except」作用域当作 try 入口。

        with 语句在 3.13 也用异常表实现清理，其条目 kind="cleanup"，
        必须排除，否则每个 with 都会被还原成 try，产出大量噪音。
        """
        off = self.ins[k].offset
        if off in self.consumed_try:
            return False
        for s, _e, _t, _d, kind in self.trys:
            if s == off:
                return kind == "except"
        return False

    def exc_type_at(self, handler_off):
        """从 handler 指令序列里取异常类型（CHECK_EXC_MATCH 前压入的名字）。"""
        seq = [i for i in self.ins if i.offset >= handler_off][:8]
        for idx, x in enumerate(seq):
            if x.opname == "CHECK_EXC_MATCH":
                for y in reversed(seq[:idx]):
                    if y.opname in ("LOAD_GLOBAL", "LOAD_NAME", "LOAD_FAST"):
                        return y.argval
                    if y.opname == "BUILD_TUPLE":
                        return "Exception"
        return "Exception"

    # ---------------------------------------------------------- 子帧辅助
    def sub(self, indent):
        """派生子帧，继承当前表达式栈状态（关键：不能重置栈）；
        并继承「已消费的 try 入口」，避免处理 try 体时无限递归。

        缩进深度保护：复杂嵌套会让缩进层数爆炸（实测出现过几十层 \t），
        超过 MAX_INDENT 时不再继续拆分结构，直接平铺并标注，保证产出可读。
        """
        s = StructGen(self.code, indent=indent)
        s.frame.stack = self.frame.stack[:]
        s.consumed_try = set(self.consumed_try)
        return s

    MAX_INDENT = 8

    def adopt(self, s):
        """把子帧产出的行接过来，并把栈状态回写（保持连续性）。"""
        body = [l for l in s.lines if l.strip()]
        self.lines.extend(body if body else
                          ["\t" * (s.indent) + "pass"])
        self.frame.stack = s.frame.stack[:]

    # ---------------------------------------------------------- for
    def gen_for(self, k, hi):
        """FOR_ITER 结构：
             <iter 表达式> 已在栈上
             FOR_ITER end
             STORE_FAST var
             ...body...
             JUMP_BACKWARD -> FOR_ITER
        """
        ins = self.ins[k]
        end_off = ins.argval
        it = self.frame.pop()
        # 循环头之后的 STORE_FAST 是循环变量
        kk = k + 1
        var = "?"
        if kk < len(self.ins) and self.ins[kk].opname in ("STORE_FAST", "STORE_NAME"):
            var = self.ins[kk].argval
            self.handled.add(self.ins[kk].offset)
            kk += 1
        self.out("for %s in %s:" % (var, it))
        # 循环体边界：找**回跳到本 FOR_ITER 的那条** JUMP_BACKWARD。
        # 不能见到 JUMP_BACKWARD 就停 —— try/except 内部常有内层回跳，
        # 会导致循环体被提前截断、后续语句错位到循环外。
        body_lo = kk
        body_hi = body_lo
        target_off = self.ins[k].offset
        while body_hi < len(self.ins):
            x = self.ins[body_hi]
            if x.opname.startswith("JUMP_BACKWARD") and x.argval == target_off:
                break
            # 若跳到更靠后的位置（内层循环），跳过它继续找本层回跳
            body_hi += 1
        body = self.sub(self.indent + 1)
        body.run(body_lo, body_hi)
        self.adopt(body)
        # 标记已处理
        for j in range(k, min(body_hi + 1, len(self.ins))):
            self.handled.add(self.ins[j].offset)
        self.handled.add(end_off)
        # 跳过 END_FOR
        kk2 = body_hi + 1
        while kk2 < len(self.ins) and self.ins[kk2].opname in ("END_FOR", "POP_TOP"):
            self.handled.add(self.ins[kk2].offset)
            kk2 += 1
        return kk2

    # ---------------------------------------------------------- if
    def gen_if(self, k, hi):
        """条件分支：
             <cond>  POP_JUMP_IF_xxx target
             ...then...
             [JUMP_FORWARD end]
             ...else...
           target / end
        """
        ins = self.ins[k]
        target_off = ins.argval
        cond = self.frame.pop()
        # POP_JUMP_IF_FALSE tgt 的语义：条件为假 → 跳 tgt。
        # 而 then 体位于 (k, tgt) 之间，即"条件为真时执行"，
        # 所以条件表达式**不需要取反**，直接输出 if cond: 即可。
        # （取反会把 if 与 else 分支弄反，导致整块缩进错位）
        if ins.opname == "POP_JUMP_IF_TRUE":
            cond = "not (%s)" % cond          # 真则跳走 → then 是"假"分支
        elif ins.opname == "POP_JUMP_IF_NONE":
            cond = "(%s is not None)" % cond  # None 则跳走 → then 是"非 None"
        elif ins.opname == "POP_JUMP_IF_NOT_NONE":
            cond = "(%s is None)" % cond

        # then 分支结束位置
        then_lo = k + 1
        then_hi = then_lo
        jump_end = None
        while then_hi < len(self.ins):
            x = self.ins[then_hi]
            if x.offset == target_off:
                break
            if x.opname.startswith("JUMP_FORWARD") and jump_end is None:
                jump_end = x.argval
                break
            then_hi += 1

        self.out("if %s:" % cond)
        then = self.sub(self.indent + 1)
        then.run(then_lo, then_hi)
        self.adopt(then)
        for j in range(k, then_hi):
            self.handled.add(self.ins[j].offset)

        nxt = then_hi
        # 有 else 分支
        if jump_end is not None:
            offs = [x.offset for x in self.ins]
            if jump_end in offs:
                e_lo = then_hi + 1 if then_hi < len(self.ins) and \
                    self.ins[then_hi].opname.startswith("JUMP_FORWARD") else then_hi
                e_hi = offs.index(jump_end)
                if e_hi > e_lo:
                    self.out("else:")
                    els = self.sub(self.indent + 1)
                    els.run(e_lo, e_hi)
                    self.adopt(els)
                    for j in range(e_lo, e_hi):
                        self.handled.add(self.ins[j].offset)
                    nxt = e_hi
        return nxt

    # ---------------------------------------------------------- try
    def gen_try(self, k, hi):
        """还原 try/except。

        3.13 的 except 样板（handler 处）：
            PUSH_EXC_INFO | LOAD_GLOBAL <Exc> | CHECK_EXC_MATCH
            | POP_JUMP_IF_FALSE <not_matched> | POP_TOP
            ...except 体...
            POP_EXCEPT | RETURN_CONST/JUMP...
            <not_matched>: RERAISE / COPY 3 | POP_EXCEPT | RERAISE 1
        """
        off = self.ins[k].offset
        scope = None
        for s, e, t, d, kind in self.trys:
            if s <= off < e and kind == "except":
                if scope is None or (e - s) < (scope[1] - scope[0]):
                    scope = (s, e, t, d)
        if scope is None:
            return k + 1
        s, e, t, d = scope
        offs = [x.offset for x in self.ins]
        if s not in offs or t not in offs:
            return k + 1
        ti, h_off = offs.index(s), offs.index(t)
        if ti != k:
            return k + 1

        exc = self.exc_type_at(self.ins[h_off].offset)
        self.consumed_try.add(s)

        # ---- try 体：handler 之前的清理样板要去掉
        try_hi = h_off
        self.out("try:")
        tb = self.sub(self.indent + 1)
        tb.consumed_try.add(s)
        tb.run(ti, try_hi)
        self.adopt(tb)

        # ---- except 体：跳过 PUSH_EXC_INFO / CHECK_EXC_MATCH 等样板
        j = h_off
        while j < hi and j < len(self.ins):
            nm = self.ins[j].opname
            if nm in ("PUSH_EXC_INFO", "CHECK_EXC_MATCH", "POP_TOP",
                      "COPY", "POP_EXCEPT", "RERAISE"):
                j += 1
                continue
            if nm in ("LOAD_GLOBAL", "LOAD_NAME", "LOAD_FAST", "BUILD_TUPLE"):
                # 异常类型 + POP_JUMP_IF_FALSE 属于样板
                nxt = self.ins[j + 1].opname if j + 1 < len(self.ins) else ""
                nxt2 = self.ins[j + 2].opname if j + 2 < len(self.ins) else ""
                if nxt in ("CHECK_EXC_MATCH", "BUILD_TUPLE") or \
                   nxt2 in ("CHECK_EXC_MATCH", "POP_JUMP_IF_FALSE"):
                    j += 1
                    continue
            if nm.startswith("POP_JUMP"):
                j += 1
                continue
            break
        body_lo = j
        # except 体结束：到 POP_EXCEPT 或 JUMP 结束
        body_hi = body_lo
        while body_hi < hi and body_hi < len(self.ins):
            nm = self.ins[body_hi].opname
            if nm in ("POP_EXCEPT", "RERAISE"):
                break
            body_hi += 1
        # 回退尾部样板
        while body_hi > body_lo and self.ins[body_hi - 1].opname in (
                "COPY", "POP_TOP", "PUSH_EXC_INFO"):
            body_hi -= 1

        self.out("except %s:" % exc)
        eb = self.sub(self.indent + 1)
        eb.consumed_try.add(s)
        eb.run(body_lo, body_hi)
        self.adopt(eb)

        # 标记整段已处理
        end = max(body_hi, h_off)
        for j in range(ti, min(end + 1, len(self.ins))):
            self.handled.add(self.ins[j].offset)
        return end + 1


def render_func_struct(fname, code, indent=0):
    """还原一个函数的完整源码（结构化版本）。"""
    ind = "\t" * indent
    # 函数体比 def 行多一级缩进
    g = StructGen(code, indent=indent + 1)
    ac, kwac = code.co_argcount, code.co_kwonlyargcount
    nv = code.co_varnames
    flags = code.co_flags
    has_va = bool(flags & 0x04)
    has_kw = bool(flags & 0x08)
    sig = list(nv[:ac])
    if has_va:
        sig.append("*" + nv[ac])
    elif kwac:
        sig.append("*")
    base = ac + (1 if has_va else 0)
    sig += list(nv[base:base + kwac])
    if has_kw:
        sig.append("**" + nv[base + kwac])
    sig = [s for s in sig if not s.startswith(".")]

    # 默认值提示（从 __defaults__ 无法直接取，标注 TODO 由人工确认）
    lines = ["%sdef %s(%s):" % (ind, fname, ", ".join(sig))]
    body = g.run()
    body = [l for l in body if l.strip()]
    lines += body if body else ["\t" * (indent + 1) + "pass"]
    return lines


def decompile(code, fname="<m>"):
    """反编译模块：识别函数/类定义，函数体走结构化还原。

    注意：模块级语句必须共用**同一个** StructGen（否则表达式栈会不断重置，
    所有赋值都变成"栈空"）。函数/类定义则单独处理。
    """
    ins = clean_ins(code)
    out = []
    g = StructGen(code, indent=0)     # 模块级共享帧（保持栈连续）
    k = 0
    while k < len(ins):
        cur = ins[k]

        # ---- def name(...)
        if (cur.opname == "LOAD_CONST"
                and isinstance(cur.argval, types.CodeType)):
            j = k + 1
            while j < len(ins) and ins[j].opname in (
                    "MAKE_FUNCTION", "SET_FUNCTION_ATTRIBUTE", "COPY"):
                j += 1
            if j < len(ins) and ins[j].opname in ("STORE_NAME", "STORE_FAST"):
                name = ins[j].argval
                out.extend(render_func_struct(name, cur.argval))
                out.append("")
                k = j + 1
                continue

        # ---- class X(Base)
        if cur.opname == "LOAD_BUILD_CLASS":
            j, cname, ccode, bases = k + 1, None, None, []
            while j < len(ins):
                it = ins[j]
                if (it.opname == "LOAD_CONST"
                        and isinstance(it.argval, types.CodeType)):
                    ccode = it.argval
                elif (it.opname == "LOAD_CONST" and isinstance(it.argval, str)
                        and cname is None):
                    cname = it.argval
                elif it.opname in ("LOAD_NAME", "LOAD_GLOBAL") and cname:
                    bases.append(it.argval)
                elif it.opname == "CALL":
                    j += 1
                    break
                j += 1
            if cname and ccode:
                out.append("class %s(%s):" % (cname, ", ".join(bases)))
                # 类体比 class 行多一级缩进
                subg = StructGen(ccode, indent=1)
                body = [l for l in subg.run() if l.strip()]
                body = [l for l in body if "__module__" not in l
                        and "__qualname__" not in l and "__firstlineno__" not in l]
                out.extend(body if body else ["\tpass"])
                out.append("")
                k = j
                continue

        # ---- 其他模块级语句：写入共享帧
        before = len(g.frame.lines)
        try:
            fn = getattr(g.frame, "i_" + cur.opname, None)
            if fn:
                fn(cur)
            else:
                g.frame.fallback(cur)
        except Exception as e:
            g.frame.fallback(cur)
        while len(g.frame.lines) > before:
            out.append(g.frame.lines.pop(before))
        k += 1
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".pyc"):
            continue
        code = marshal.loads(open(os.path.join(src, fn), "rb").read()[16:])
        lines = decompile(code, fn)
        text = "\n".join(lines) + "\n"
        try:
            compile(text, fn[:-4] + ".py", "exec")
            mark = "OK"
        except SyntaxError as e:
            mark = "语法问题 L%s" % e.lineno
        out = os.path.join(dst, fn[:-4] + ".py")
        open(out, "w", encoding="utf-8").write(text)
        todo = text.count("[未实现]") + text.count("[控制流]") + text.count("[无法还原]")
        print("[*] %-20s %4d 行  待补=%-4d %s" % (fn, text.count("\n"), todo, mark))
    return 0


if __name__ == "__main__":
    sys.exit(main())
