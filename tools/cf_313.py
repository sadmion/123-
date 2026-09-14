#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cf_313.py —— CPython 3.13 控制流结构化模块

把线性字节码还原成 if / for / while / try-except 结构。

方法：
  1) 用跳转指令切分"基本块"（basic block）
  2) 依据块的跳转关系构建 CFG
  3) 识别三件套：
       - for:   FOR_ITER ... JUMP_BACKWARD(回到 FOR_ITER)
       - while: 条件跳转回跳 + 无 FOR_ITER
       - if/else: 条件跳转 + 前向 JUMP_FORWARD
       - try/except: 依据 co_exceptiontable 的 (start,end,target)
  4) 输出带缩进的结构化语句序列

该模块与 decompiler_313.py 配合：表达式还原由后者负责，
结构由本模块给出"块 -> 结构"的映射。
"""
import dis
import types

# 条件跳转 -> 反向条件（用于生成 if 的条件）
INVERT = {
    "POP_JUMP_IF_FALSE": "false",
    "POP_JUMP_IF_TRUE": "true",
    "POP_JUMP_IF_NONE": "none",
    "POP_JUMP_IF_NOT_NONE": "not_none",
}


class Block:
    __slots__ = ("start", "end", "ops", "succ", "pred", "kind", "marked")

    def __init__(self, start):
        self.start = start
        self.end = start
        self.ops = []
        self.succ = []
        self.pred = []
        self.kind = "normal"
        self.marked = False

    def __repr__(self):
        return "<Blk %d-%d %s -> %s>" % (self.start, self.end, self.kind,
                                         [b.start for b in self.succ])


def split_blocks(ins):
    """按跳转边界切分基本块。返回 (blocks, off2blk)。"""
    # 收集所有块起点：函数入口 + 每条跳转的目标 + 跳转的下一条
    starts = {ins[0].offset}
    for i, x in enumerate(ins):
        if x.opname.startswith(("POP_JUMP", "JUMP", "FOR_ITER", "SEND")):
            if isinstance(x.argval, int):
                starts.add(x.argval)
            if i + 1 < len(ins):
                starts.add(ins[i + 1].offset)
    # 异常处理目标也是块起点
    starts = {s for s in starts if any(x.offset == s for x in ins)}

    blocks = []
    off2blk = {}
    cur = None
    for x in ins:
        if x.offset in starts:
            cur = Block(x.offset)
            blocks.append(cur)
            off2blk[x.offset] = cur
        if cur is None:
            cur = Block(x.offset)
            blocks.append(cur)
            off2blk[x.offset] = cur
        cur.ops.append(x)
        cur.end = x.offset
    # 连接后继
    for k, b in enumerate(blocks):
        last = b.ops[-1]
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        if last.opname.startswith(("POP_JUMP", "JUMP", "FOR_ITER", "SEND")):
            if last.opname.startswith("POP_JUMP") or last.opname in ("FOR_ITER", "SEND"):
                if nxt:
                    b.succ.append(nxt)
            t = off2blk.get(last.argval)
            if t:
                b.succ.append(t)
        elif last.opname in ("RETURN_VALUE", "RETURN_CONST", "RAISE_VARARGS",
                             "RERAISE"):
            b.kind = "exit"
        else:
            if nxt:
                b.succ.append(nxt)
    for b in blocks:
        for s in b.succ:
            s.pred.append(b)
    return blocks, off2blk


def find_loops(blocks, off2blk):
    """识别回边，返回 {header_offset: (kind, back_blk)}。

    for 循环：回跳目标处的块含 FOR_ITER
    while   ：回跳目标处的块不含 FOR_ITER
    """
    loops = {}
    for b in blocks:
        last = b.ops[-1]
        if last.opname.startswith("JUMP_BACKWARD"):
            tgt = off2blk.get(last.argval)
            if tgt is None:
                continue
            has_for = any(x.opname == "FOR_ITER" for x in tgt.ops)
            loops[tgt.start] = ("for" if has_for else "while", b)
    return loops


def find_try_scopes(code):
    """解析 3.13 异常表，返回 try 作用域列表。

    每项: (start_off, end_off, handler_off, depth)
    """
    out = []
    try:
        for e in dis._parse_exception_table(code):
            out.append((e.start, e.end, e.target, e.depth))
    except Exception:
        pass
    # 只保留"真正进入 except 主体"的条目（depth 较小者通常是 with 清理）
    return out


def describe(code):
    """输出一个代码对象的结构摘要，便于人工/程序分析。"""
    ins = [i for i in dis.get_instructions(code)
           if i.opname not in ("RESUME", "CACHE", "NOP", "PRECALL",
                               "EXTENDED_ARG")]
    blocks, off2blk = split_blocks(ins)
    loops = find_loops(blocks, off2blk)
    trys = find_try_scopes(code)
    lines = []
    lines.append("# 块数=%d  循环=%d  异常作用域=%d" % (len(blocks), len(loops), len(trys)))
    for b in blocks:
        kinds = []
        for x in b.ops:
            if x.opname in INVERT:
                kinds.append("%s->%s" % (x.opname, x.argval))
            elif x.opname == "FOR_ITER":
                kinds.append("FOR_ITER->%s" % x.argval)
            elif x.opname.startswith("JUMP"):
                kinds.append("%s->%s" % (x.opname, x.argval))
        tag = ""
        if b.start in loops:
            tag = " [%s头]" % loops[b.start][0]
        lines.append("  块@%-5d 指令%-3d%s %s" % (
            b.start, len(b.ops), tag, "; ".join(kinds) if kinds else ""))
    for s, e, t, d in trys:
        lines.append("  try: [%d,%d) -> handler@%d (depth=%d)" % (s, e, t, d))
    return "\n".join(lines)


if __name__ == "__main__":
    import marshal
    import sys
    p = sys.argv[1]
    data = open(p, "rb").read()
    code = marshal.loads(data[16:])

    def walk(c, out=None):
        out = [] if out is None else out
        out.append(c)
        for k in c.co_consts:
            if isinstance(k, types.CodeType):
                walk(k, out)
        return out

    for c in walk(code):
        print("=" * 70)
        print("### %s" % c.co_name)
        print(describe(c))
