#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""影库瘦身 / 拆分工具 —— 解决「追加影库闪退」

## 问题

程序用 `json.load` 一次性全量解析影库并常驻内存。实测：

| 影库 | 文件大小 | 记录数 | 加载内存 | 峰值 |
|---|---|---|---|---|
| 合并影库 | 192.7 MB | 746,686 | 708 MB | **1,495 MB** |

**峰值可达文件体积的 8 倍。** 追加新影库时内存叠加，超过可用内存即被系统杀掉
（表现为：网页点「追加影库」后程序闪退）。

## 解决思路

单个影库越小，解析峰值越低。本工具把大影库拆成多个小影库：

- 每个子库建议 **≤ 5 万条**（峰值约 100 MB，安全）
- 也可用 `--sample` 按比例抽样，快速瘦身
- 输出文件可直接放进「秒传文件导入或追加」目录

## 用法

    # 查看影库信息（不修改）
    python 影库瘦身.py "影库.json" --info

    # 按条数拆成多个小库（每个最多 5 万条）
    python 影库瘦身.py "影库.json" --split 50000

    # 按顶级目录拆分（保持分类结构，组内超限再切块）
    python 影库瘦身.py "影库.json" --split-by-dir 50000

    # 只保留指定前缀的内容
    python 影库瘦身.py "影库.json" --filter "电影/"

    # 抽样 30%（快速瘦身，随机保留）
    python 影库瘦身.py "影库.json" --sample 0.3

    # 组合：先过滤再拆分
    python 影库瘦身.py "影库.json" --filter "剧集/" --split 50000

输出目录默认 `瘦身输出/`，用 `--out-dir` 指定。
**默认不修改原文件。**
"""
import argparse
import json
import os
import random
import sys

# 单个子库的建议上限：5 万条时解析峰值约 100MB
SAFE_LIMIT = 50000


def human(n):
    for u, s in (("TB", 1024 ** 4), ("GB", 1024 ** 3), ("MB", 1024 ** 2), ("KB", 1024)):
        if n >= s:
            return "%.2f %s" % (n / s, u)
    return "%d B" % n


def norm(p):
    return (p or "").replace("\\", "/")


def top_group(common, path):
    """按 commonPath 之后的第一层目录分组。"""
    p = norm(path)
    cp = norm(common)
    if cp and p.startswith(cp):
        p = p[len(cp):]
    parts = [x for x in p.strip("/").split("/") if x]
    return parts[0] if len(parts) > 1 else "(未分类)"


def safe_name(s):
    return "".join(c if c not in '\\/:*?"<>|' else "-" for c in s)


def build_lib(src, files, name, common=None):
    total = sum(int(f.get("size") or 0) for f in files)
    return {
        "scriptVersion": src.get("scriptVersion", "3.2.0-tdr.3"),
        "exportVersion": src.get("exportVersion", "1.0"),
        "usesBase62EtagsInExport": src.get("usesBase62EtagsInExport", True),
        "commonPath": common if common is not None else src.get("commonPath", ""),
        "totalFilesCount": len(files),
        "totalSize": total,
        "formattedTotalSize": human(total),
        "files": files,
    }


def main():
    ap = argparse.ArgumentParser(
        description="影库瘦身/拆分（缓解追加影库时的内存闪退）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lib", help="要处理的 .123fastlink.json / .json 影库")
    ap.add_argument("--info", action="store_true", help="只查看信息")
    ap.add_argument("--split", type=int, metavar="N",
                    help="按条数拆分，每库最多 N 条（建议 %d）" % SAFE_LIMIT)
    ap.add_argument("--split-by-dir", type=int, metavar="N",
                    help="按顶级目录拆分，组内超 N 条再切块")
    ap.add_argument("--filter", default="", help="只保留 path 以此开头的记录")
    ap.add_argument("--sample", type=float, metavar="R",
                    help="随机抽样比例 0~1，如 0.3")
    ap.add_argument("--seed", type=int, default=42, help="抽样随机种子")
    ap.add_argument("--out-dir", default="瘦身输出", help="输出目录")
    ap.add_argument("--dry-run", action="store_true", help="只预览不写出")
    a = ap.parse_args()

    if not os.path.isfile(a.lib):
        print("找不到文件: %s" % a.lib)
        return 2

    size_mb = os.path.getsize(a.lib) / 1048576
    print("读取 %s (%.1f MB) ..." % (os.path.basename(a.lib), size_mb))
    with open(a.lib, encoding="utf-8") as f:
        d = json.load(f)
    files = d.get("files") or []
    common = d.get("commonPath", "")
    base = os.path.splitext(os.path.basename(a.lib))[0]
    if base.endswith(".123fastlink"):
        base = base[:-len(".123fastlink")]

    print()
    print("=" * 66)
    print(" 影库信息")
    print("=" * 66)
    print("  记录数    : %d" % len(files))
    print("  总体积    : %s" % d.get("formattedTotalSize", "-"))
    print("  commonPath: %r" % common)
    # 内存估算（实测约 8 倍文件体积峰值）
    print("  加载内存  : ≈ %.0f MB（峰值）" % (size_mb * 7.8))
    if size_mb * 7.8 > 800:
        print("  ⚠ 该影库加载峰值较高，建议拆分后再导入")
    print()

    if a.info:
        groups = {}
        for f in files:
            groups[top_group(common, f.get("path"))] = \
                groups.get(top_group(common, f.get("path")), 0) + 1
        top = sorted(groups.items(), key=lambda x: -x[1])[:15]
        print("  顶级分组（前 15）:")
        for k, v in top:
            print("    %-44s %7d 条" % (k[:44], v))
        if len(groups) > 15:
            print("    ... 共 %d 个分组" % len(groups))
        return 0

    # ---- 过滤
    if a.filter:
        pre = norm(a.filter)
        files = [f for f in files if norm(f.get("path")).startswith(pre)]
        print("按前缀 %r 过滤后: %d 条" % (a.filter, len(files)))
        if not files:
            print("没有匹配记录。")
            return 1

    # ---- 抽样
    if a.sample is not None:
        if not 0 < a.sample <= 1:
            print("--sample 应在 (0,1] 之间")
            return 2
        rnd = random.Random(a.seed)
        keep = int(len(files) * a.sample)
        files = rnd.sample(files, keep)
        print("抽样 %.0f%% 后: %d 条" % (a.sample * 100, len(files)))

    # ---- 分组
    groups = []
    if a.split_by_dir:
        per = a.split_by_dir
        buckets = {}
        for f in files:
            buckets.setdefault(top_group(common, f.get("path")), []).append(f)
        for g in sorted(buckets):
            items = buckets[g]
            if len(items) <= per:
                groups.append(("%s_%s" % (base, g), items))
            else:
                for i in range(0, len(items), per):
                    groups.append(("%s_%s_part%02d" % (base, g, i // per + 1),
                                   items[i:i + per]))
    elif a.split:
        per = a.split
        for i in range(0, len(files), per):
            groups.append(("%s_part%02d" % (base, i // per + 1),
                           files[i:i + per]))
    else:
        groups = [(base, files)]

    # ---- 预览
    print()
    print("=" * 66)
    print(" 拆分结果：%d 个%s" % (len(groups), "（预览，未写出）" if a.dry_run else ""))
    print("=" * 66)
    total = 0
    for name, g in groups:
        total += len(g)
        sz = sum(int(f.get("size") or 0) for f in g)
        est = len(g) * 1024 / 1048576   # 约 1KB/条
        print("  %-46s %6d 条  %-10s 内存≈%.0fMB"
              % (name[:46], len(g), human(sz), est))
    print("-" * 66)
    print("  合计 %d 条" % total)

    if not a.dry_run:
        os.makedirs(a.out_dir, exist_ok=True)
        print()
        for name, g in groups:
            fn = safe_name(name)
            if not fn.lower().endswith(".json"):
                fn += ".123fastlink.json"
            out = os.path.join(a.out_dir, fn)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(build_lib(d, g, name), f, ensure_ascii=False)
            print("  已写出 %-52s %.1f MB" % (fn[:52], os.path.getsize(out) / 1048576))
        print()
        print("=" * 66)
        print(" 完成。把输出文件放进「秒传文件导入或追加」目录即可。")
        print(" 注意：导入前建议先移走原有的超大影库，避免内存叠加。")
        print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
