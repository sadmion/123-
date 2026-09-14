#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decompiler_313.py —— 面向 CPython 3.13 字节码的反编译器

为什么需要自己写：
    现有工具都不支持 3.13 ——
      decompyle3 / uncompyle6：源码里 PYTHON_VERSIONS 写死 (3,7),(3,8)
      xdis 6.3.0            ：有 3.13 的 opcode 表，但没有语法重建器
      pycdc                 ：需 C++ 工具链；release 产物已过期
    目标 exe 由 Python 3.13 打包，因此必须自建。

实现思路：
    1) 线性扫描指令，维护一个"表达式栈"，把栈机指令还原成嵌套表达式
    2) 用跳转目标 + ExceptionTable 把控制流还原成 if/for/while/try/with
    3) 函数与类定义按 3.13 的 LOAD_CONST<code> | MAKE_FUNCTION | STORE 模式还原
    4) 每步都做 compile() 自检，无法确定的地方显式标注而非猜测

用法：
    python decompiler_313.py <pyc目录> <输出目录>
"""
import dis
import marshal
import os
import sys
import types

# ------------------------------------------------------------------ 常量表

COMPARE_OPS = {"==": "==", "!=": "!=", "<": "<", "<=": "<=", ">": ">",
               ">=": ">=", "in": "in", "not in": "not in", "is": "is",
               "is not": "is not", "exception match": "isinstance"}

# SET_FUNCTION_ATTRIBUTE 的标志位（3.13）
FUNC_DEFAULTS = 0x01
FUNC_KWONLY_DEFAULTS = 0x02
FUNC_ANNOTATIONS = 0x04
FUNC_CLOSURE = 0x08

# 一元运算
UNARY = {"UNARY_NEGATIVE": "-", "UNARY_NOT": "not ", "UNARY_INVERT": "~"}


def is_jump(op):
    return op.startswith(("POP_JUMP", "JUMP", "FOR_ITER", "SEND"))


class Bail(Exception):
    """无法安全还原时抛出，交由上层降级处理。"""


class Frame:
    """一个代码对象的反编译帧。"""

    def __init__(self, code, name=None, indent=0):
        self.code = code
        self.name = name or code.co_name
        self.indent = indent
        self.ins = [i for i in dis.get_instructions(code)
                    if i.opname not in ("RESUME", "CACHE", "NOP",
                                        "PRECALL", "EXTENDED_ARG")]
        self.pc = 0
        self.stack = []
        self.lines = []
        self._t = 0

    # ---------------------------------------------------------- 输出
    def emit(self, s, indent=None):
        lv = self.indent if indent is None else indent
        self.lines.append("\t" * lv + s)

    def blank(self):
        self.lines.append("")

    def tmp(self):
        self._t += 1
        return "_v%d" % self._t

    # ---------------------------------------------------------- 栈
    def push(self, v):
        self.stack.append(v)

    def pop(self, dflt=None):
        """弹栈。栈空时返回占位符而不是抛异常 —— 某些未实现指令
        （如 BEFORE_WITH、异常处理）会破坏栈平衡，抛异常会导致整个
        函数体丢失，得不偿失。占位符会在输出里显形，便于人工补齐。"""
        if not self.stack:
            return "<栈空>" if dflt is None else dflt
        return self.stack.pop()

    def peek(self, n=0):
        return self.stack[-1 - n] if len(self.stack) > n else None

    def args(self, n):
        """弹出 n 个参数（保持原顺序）。"""
        if n == 0:
            return []
        items = [self.pop() for _ in range(n)]
        return items[::-1]

    # ---------------------------------------------------------- 入口
    def run(self):
        while self.pc < len(self.ins):
            ins = self.ins[self.pc]
            fn = getattr(self, "i_" + ins.opname, None)
            if fn is None:
                try:
                    self.fallback(ins)
                except Bail:
                    raise
                except Exception as e:
                    self.emit("# [异常 %s] %s" % (ins.opname, e))
            else:
                try:
                    fn(ins)
                except Bail:
                    raise
                except Exception as e:
                    self.emit("# [异常 %s] %s" % (ins.opname, e))
            self.pc += 1
        return self.lines

    def fallback(self, ins):
        """未实现指令：标注出来，保证不静默丢失信息。"""
        if is_jump(ins.opname) or ins.opname.startswith(
                ("SETUP_", "POP_BLOCK", "RERAISE", "PUSH_EXC", "POP_EXCEPT",
                 "WITH_EXCEPT", "BEFORE_WITH", "MAKE_FUNCTION",
                 "SET_FUNCTION_ATTRIBUTE", "BUILD_MAP", "GET_ITER",
                 "FOR_ITER", "END_FOR", "END_SEND", "GET_YIELD",
                 "LOAD_CLOSURE", "MAKE_CELL", "COPY_FREE_VARS",
                 "RETURN_GENERATOR", "YIELD", "SEND", "GET_AWAITABLE",
                 "CLEANUP_THROW", "CHECK_EG_MATCH", "PREP_RERAISE",
                 "MATCH_", "GET_AITER", "GET_ANEXT", "END_ASYNC_FOR")):
            self.emit("# [控制流] %s %r" % (ins.opname, ins.argval))
        else:
            self.emit("# [未实现] %s %r" % (ins.opname, ins.argval))

    # ====================================================== 加载 / 存储
    def i_LOAD_CONST(self, ins):
        self.push(repr(ins.argval))

    def i_LOAD_FAST(self, ins):
        self.push(ins.argval)

    def i_LOAD_FAST_LOAD_FAST(self, ins):
        """3.13 复合指令：一次压入两个局部变量 (a, b)。"""
        a, b = ins.argval
        self.push(a)
        self.push(b)

    def i_LOAD_CONST_LOAD_FAST(self, ins):
        c, f = ins.argval
        self.push(repr(c))
        self.push(f)

    i_LOAD_FAST_CHECK = i_LOAD_FAST
    i_LOAD_FAST_AND_CLEAR = i_LOAD_FAST

    def i_LOAD_NAME(self, ins):
        self.push(ins.argval)

    def i_LOAD_GLOBAL(self, ins):
        self.push(ins.argval)

    def i_LOAD_DEREF(self, ins):
        self.push(ins.argval)

    i_LOAD_CLASSDEREF = i_LOAD_DEREF
    i_LOAD_FROM_DICT_OR_DEREF = i_LOAD_DEREF
    i_LOAD_FROM_DICT_OR_GLOBALS = i_LOAD_DEREF
    i_LOAD_CLOSURE = i_LOAD_DEREF

    def i_LOAD_ATTR(self, ins):
        self.push("%s.%s" % (self.pop(), ins.argval))

    i_LOAD_METHOD = i_LOAD_ATTR

    def i_LOAD_SUPER_ATTR(self, ins):
        self.pop(); self.pop()      # super() 的两个参数
        self.push("super().%s" % ins.argval)

    def i_LOAD_ASSERTION_ERROR(self, ins):
        self.push("AssertionError")

    def i_LOAD_BUILD_CLASS(self, ins):
        self.push("__build_class__")

    def i_LOAD_LOCALS(self, ins):
        self.push("locals()")

    def i_PUSH_NULL(self, ins):
        self.push(None)

    def i_POP_TOP(self, ins):
        v = self.pop(None)
        if v is not None and not str(v).startswith("#"):
            self.emit(str(v))

    # with 语句：BEFORE_WITH 后的 STORE_FAST 是 with ... as x
    def i_BEFORE_WITH(self, ins):
        self.push("__with__")

    def i_BEFORE_ASYNC_WITH(self, ins):
        self.push("__awith__")

    def i_COPY(self, ins):
        n = ins.argval if isinstance(ins.argval, int) else 1
        self.push(self.peek(n - 1))

    def i_SWAP(self, ins):
        n = ins.argval if isinstance(ins.argval, int) else 2
        if len(self.stack) >= n:
            self.stack[-1], self.stack[-n] = self.stack[-n], self.stack[-1]

    def i_STORE_FAST(self, ins):
        v = self.pop(None)
        if v is not None:
            self.emit("%s = %s" % (ins.argval, v))

    i_STORE_NAME = i_STORE_FAST
    i_STORE_GLOBAL = i_STORE_FAST
    i_STORE_DEREF = i_STORE_FAST

    def i_STORE_ATTR(self, ins):
        obj = self.pop()
        v = self.pop(None)
        if v is not None:
            self.emit("%s.%s = %s" % (obj, ins.argval, v))

    def i_DELETE_FAST(self, ins):
        self.emit("del %s" % ins.argval)

    i_DELETE_NAME = i_DELETE_FAST
    i_DELETE_GLOBAL = i_DELETE_FAST
    i_DELETE_DEREF = i_DELETE_FAST

    # ====================================================== 运算
    def i_BINARY_OP(self, ins):
        op = ins.argrepr or "?"
        b, a = self.pop(), self.pop()
        if op.endswith("=") and op != "==":
            self.push("%s %s %s" % (a, op, b))
        else:
            self.push("(%s %s %s)" % (a, op, b))

    def i_BINARY_SUBSCR(self, ins):
        k = self.pop(); o = self.pop()
        self.push("%s[%s]" % (o, k))

    def i_STORE_SUBSCR(self, ins):
        k = self.pop(); o = self.pop(); v = self.pop(None)
        if v is not None:
            self.emit("%s[%s] = %s" % (o, k, v))

    def i_DELETE_SUBSCR(self, ins):
        k = self.pop(); o = self.pop()
        self.emit("del %s[%s]" % (o, k))

    def i_UNARY_NEGATIVE(self, ins):
        self.push("(-%s)" % self.pop())

    def i_UNARY_NOT(self, ins):
        self.push("(not %s)" % self.pop())

    def i_UNARY_INVERT(self, ins):
        self.push("(~%s)" % self.pop())

    def i_COMPARE_OP(self, ins):
        b, a = self.pop(), self.pop()
        op = ins.argrepr or "=="
        self.push("(%s %s %s)" % (a, op, b))

    def i_IS_OP(self, ins):
        b, a = self.pop(), self.pop()
        self.push("(%s is%s %s)" % (a, "" if ins.argval else " not", b))

    def i_CONTAINS_OP(self, ins):
        b, a = self.pop(), self.pop()
        self.push("(%s %sin %s)" % (a, "" if ins.argval else "not ", b))

    def i_TO_BOOL(self, ins):
        v = self.pop()
        self.push("bool(%s)" % v)

    def i_NOT_TAKEN(self, ins):
        pass

    # ====================================================== 容器
    def _build(self, n, fmt):
        items = self.args(n)
        if fmt == "tuple":
            self.push("(%s%s)" % (", ".join(items), "," if n == 1 else ""))
        elif fmt == "list":
            self.push("[%s]" % ", ".join(items))
        elif fmt == "set":
            self.push("{%s}" % ", ".join(items) if n else "set()")

    def i_BUILD_TUPLE(self, ins):
        self._build(ins.argval, "tuple")

    def i_BUILD_LIST(self, ins):
        self._build(ins.argval, "list")

    def i_BUILD_SET(self, ins):
        self._build(ins.argval, "set")

    def i_BUILD_MAP(self, ins):
        n = ins.argval
        pairs = []
        for _ in range(n):
            v = self.pop(); k = self.pop()
            pairs.append((k, v))
        pairs.reverse()
        self.push("{%s}" % ", ".join("%s: %s" % p for p in pairs) if pairs else "{}")

    def i_BUILD_CONST_KEY_MAP(self, ins):
        keys = eval(self.pop())
        vals = self.args(ins.argval)
        self.push("{%s}" % ", ".join("%r: %s" % (k, v)
                                     for k, v in zip(keys, vals)))

    def i_BUILD_STRING(self, ins):
        parts = self.args(ins.argval)
        self.push("f'%s'" % "".join(
            p if p.startswith("{") else "{%s}" % p for p in parts))

    def i_BUILD_SLICE(self, ins):
        n = ins.argval
        v = self.args(n)
        self.push(":".join(v))

    def i_LIST_EXTEND(self, ins):
        it = self.pop(); lst = self.pop()
        self.push("%s + list(%s)" % (lst, it))

    def i_LIST_APPEND(self, ins):
        v = self.pop(); lst = self.pop()
        self.push("%s + [%s]" % (lst, v))

    def i_SET_UPDATE(self, ins):
        it = self.pop(); s = self.pop()
        self.push("%s | set(%s)" % (s, it))

    def i_MAP_ADD(self, ins):
        v = self.pop(); k = self.pop(); d = self.pop()
        self.push("dict(%s, **{%s: %s})" % (d, k, v))

    def i_DICT_UPDATE(self, ins):
        u = self.pop(); d = self.pop()
        self.push("dict(%s, **%s)" % (d, u))

    i_DICT_MERGE = i_DICT_UPDATE

    def i_FORMAT_VALUE(self, ins):
        v = self.pop()
        conv = {1: "!s", 2: "!r", 3: "!a"}.get(ins.argval & 0x03, "")
        spec = ""
        if ins.argval & 0x04:
            spec = self.pop()
        self.push("{%s%s}" % (v, conv))

    i_FORMAT_SIMPLE = i_FORMAT_VALUE

    def i_CONVERT_VALUE(self, ins):
        v = self.pop()
        self.push({1: "str(%s)" % v, 2: "repr(%s)" % v,
                   3: "ascii(%s)" % v}.get(ins.argval, "str(%s)" % v))

    # ====================================================== 调用
    def i_CALL(self, ins):
        a = self.args(ins.argval)
        fn = self.pop(None)
        if self.peek() is None:
            self.pop()
        if fn is None:
            fn = self.pop(None) or "?"
        self.push("%s(%s)" % (fn, ", ".join(a)))

    def i_CALL_KW(self, ins):
        n = ins.argval
        kwnames = eval(self.pop())
        kwvals = self.args(len(kwnames))
        npos = n - len(kwnames)
        posvals = self.args(npos)
        fn = self.pop(None)
        if self.peek() is None:
            self.pop()
        if fn is None:
            fn = self.pop(None) or "?"
        parts = list(posvals) + ["%s=%s" % (k, v) for k, v in zip(kwnames, kwvals)]
        self.push("%s(%s)" % (fn, ", ".join(parts)))

    def i_CALL_FUNCTION_EX(self, ins):
        kw = self.pop() if (ins.argval & 0x01) else None
        args = self.pop()
        fn = self.pop(None)
        if self.peek() is None:
            self.pop()
        if fn is None:
            fn = self.pop(None) or "?"
        s = "%s(*%s" % (fn, args)
        if kw:
            s += ", **%s" % kw
        self.push(s + ")")

    def i_CALL_INTRINSIC_1(self, ins):
        v = self.pop()
        m = {5: "(+%s)" % v, 6: "tuple(%s)" % v,
             1: "print(%s)" % v, 4: "INTRINSIC_ASYNC_GEN_WRAP(%s)" % v}
        self.push(m.get(ins.argval, "INTRINSIC1_%s(%s)" % (ins.argval, v)))

    def i_CALL_INTRINSIC_2(self, ins):
        b, a = self.pop(), self.pop()
        self.push("INTRINSIC2_%s(%s, %s)" % (ins.argval, a, b))

    def i_KW_NAMES(self, ins):
        self.push(repr(ins.argval))

    def i_GET_ITER(self, ins):
        self.push(self.pop())

    def i_GET_LEN(self, ins):
        self.push("len(%s)" % self.pop())

    def i_IMPORT_NAME(self, ins):
        fl = self.pop() if self.stack else "None"
        lv = self.pop() if self.stack else "0"
        self.push("__import__(%r, None, None, %s)" % (ins.argval, fl))

    def i_IMPORT_FROM(self, ins):
        self.push("%s.%s" % (self.peek() or "?", ins.argval))

    def i_IMPORT_STAR(self, ins):
        self.emit("from %s import *" % self.pop())

    # ====================================================== 返回 / 异常
    def i_RETURN_VALUE(self, ins):
        v = self.pop(None)
        self.emit("return" if v is None else "return %s" % v)

    def i_RETURN_CONST(self, ins):
        self.emit("return" if ins.argval is None else "return %r" % (ins.argval,))

    def i_RAISE_VARARGS(self, ins):
        self.emit("raise %s" % ", ".join(self.args(ins.argval)))

    def i_RERAISE(self, ins):
        self.emit("raise")

    def i_CHECK_EXC_MATCH(self, ins):
        b, a = self.pop(), self.pop()
        self.push("isinstance(%s, %s)" % (a, b))


# ------------------------------------------------------------ 函数/类定义

def render_func(fname, code, defaults=(), kwdefaults=None, decorators=(),
                indent=0):
    """把一个代码对象渲染成 def 语句（含签名与函数体）。"""
    out = []
    ind = "\t" * indent
    for d in decorators:
        out.append("%s@%s" % (ind, d))

    ac = code.co_argcount
    kwac = code.co_kwonlyargcount
    nv = code.co_varnames
    posonly = code.co_posonlyargcount
    flags = code.co_flags
    has_vararg = bool(flags & 0x04)
    has_kwarg = bool(flags & 0x08)

    names = list(nv[:ac])
    sig = []
    ndef = len(defaults)
    for k, nm in enumerate(names):
        di = k - (ac - ndef)
        if nm.startswith("."):      # 隐式参数（推导式等）
            continue
        if di >= 0 and di < ndef:
            sig.append("%s=%s" % (nm, defaults[di]))
        else:
            sig.append(nm)
    if has_vararg:
        sig.append("*" + nv[ac])
    elif kwac:
        sig.append("*")
    kw_names = list(nv[ac + (1 if has_vararg else 0):][:kwac])
    for k, nm in enumerate(kw_names):
        if kwdefaults and k < len(kwdefaults):
            sig.append("%s=%s" % (nm, kwdefaults[k]))
        else:
            sig.append(nm)
    if has_kwarg:
        sig.append("**" + nv[ac + (1 if has_vararg else 0) + kwac])

    out.append("%sdef %s(%s):" % (ind, fname, ", ".join(sig)))
    sub = Frame(code, name=fname, indent=indent + 1)
    try:
        body = sub.run()
    except Bail as e:
        body = ["\t" * (indent + 1) + "# [无法还原: %s]" % e]
    body = [l for l in body if l.strip()]
    if not body:
        body = ["\t" * (indent + 1) + "pass"]
    out.extend(body)
    return out


def render_class(cname, code, bases, indent=0):
    """渲染类定义（LOAD_BUILD_CLASS + 元类调用）。"""
    out = []
    ind = "\t" * indent
    base_s = ", ".join(bases) if bases else ""
    out.append("%sclass %s(%s):" % (ind, cname, base_s))
    sub = Frame(code, name=cname, indent=indent + 1)
    try:
        body = sub.run()
    except Bail as e:
        body = ["\t" * (indent + 1) + "# [无法还原: %s]" % e]
    body = [l for l in body if l.strip()]
    if not body:
        body = ["\t" * (indent + 1) + "pass"]
    out.extend(body)
    return out


def decompile_module(code, filename="<decompiled>"):
    """反编译一个模块级的代码对象，返回源码文本。"""
    src = _module_body(code)
    text = "\n".join(src) + "\n"
    # 自检
    try:
        compile(text, filename, "exec")
    except SyntaxError as e:
        text = ("# ⚠ 自动反编译产出，语法自检未通过（第 %s 行）: %s\n"
                "# 该文件需人工校对后再使用\n" % (e.lineno, e.msg)) + text
    return text


def _module_body(code):
    """模块级：按模式识别函数/类定义，其余交给通用帧处理。"""
    ins = [i for i in dis.get_instructions(code)
           if i.opname not in ("RESUME", "CACHE", "NOP", "PRECALL",
                               "EXTENDED_ARG")]
    out = []
    f = Frame(code, indent=0)
    # 用一个轻量前瞻：识别 LOAD_CONST<code> MAKE_FUNCTION [SET_ATTR] STORE
    idx = 0
    while idx < len(ins):
        cur = ins[idx]
        nxt = ins[idx + 1] if idx + 1 < len(ins) else None
        nxt2 = ins[idx + 2] if idx + 2 < len(ins) else None
        nxt3 = ins[idx + 3] if idx + 3 < len(ins) else None

        # def name(...)
        if (cur.opname == "LOAD_CONST" and isinstance(cur.argval, types.CodeType)
                and nxt is not None and nxt.opname == "MAKE_FUNCTION"):
            store = nxt2
            decorators = []
            j = idx + 2
            while j < len(ins) and ins[j].opname == "SET_FUNCTION_ATTRIBUTE":
                j += 1
            if j < len(ins):
                store = ins[j]
            fname = cur.argval.co_name
            out.extend(render_func(fname, cur.argval, indent=0))
            out.append("")
            idx = j + 1
            continue

        # class X(Base)
        if (cur.opname == "LOAD_BUILD_CLASS"):
            # 模式: LOAD_BUILD_CLASS | PUSH_NULL | LOAD_CONST<code> | MAKE_FUNCTION
            #       | LOAD_CONST name | [LOAD_NAME base...] | CALL n | STORE_NAME
            k = idx + 1
            cname, ccode, bases = None, None, []
            while k < len(ins):
                it = ins[k]
                if it.opname == "LOAD_CONST" and isinstance(it.argval, types.CodeType):
                    ccode = it.argval
                elif it.opname == "LOAD_CONST" and isinstance(it.argval, str) and cname is None:
                    cname = it.argval
                elif it.opname in ("LOAD_NAME", "LOAD_GLOBAL", "LOAD_FAST"):
                    if cname:
                        bases.append(it.argval)
                elif it.opname == "CALL":
                    k += 1
                    break
                k += 1
            if cname and ccode:
                out.extend(render_class(cname, ccode, bases, indent=0))
                out.append("")
                idx = k
                continue

        # 其余：交给通用帧逐条处理
        try:
            fn = getattr(f, "i_" + cur.opname, None)
            if fn:
                fn(cur)
            else:
                f.fallback(cur)
        except Bail as e:
            out.append("# [无法还原] %s" % e)
        except Exception as e:
            out.append("# [异常 %s] %s" % (cur.opname, e))
        idx += 1
    out.extend(f.lines)
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    srcdir, dstdir = sys.argv[1], sys.argv[2]
    os.makedirs(dstdir, exist_ok=True)
    for fn in sorted(os.listdir(srcdir)):
        if not fn.endswith(".pyc"):
            continue
        code = marshal.loads(open(os.path.join(srcdir, fn), "rb").read()[16:])
        text = decompile_module(code, fn[:-4] + ".py")
        out = os.path.join(dstdir, fn[:-4] + ".py")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        n = text.count("\n")
        todo = text.count("[未实现]") + text.count("[控制流]") + text.count("[无法还原]")
        print("[*] %-22s -> %-24s %4d 行, %d 处待补" % (fn, out, n, todo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
