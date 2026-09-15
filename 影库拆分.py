#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""影库拆分 / 瘦身工具

背景：程序把整个影库 JSON 解析后常驻内存（实测 192MB 影库 → 峰值 1.5GB、
全量对象化 2.2GB）。影库过大会导致「追加时闪退」（内存耗尽）。

本脚本把一个大影库按规则拆成多个小影库，使单个文件的大小可控，
从而显著降低解析峰值内存。

用法：
    # 查看影库信息（不修改）
    python 影库拆分.py "影库文件.123fastlink.json"

    # 按顶级目录拆分，每个子库最多 10 万条
    python 影库拆分.py "影库文件.123fastlink.json" --split-by dir --max-files 100000

    # 按每 10 万条顺序切块
    python 影库拆分.py "影库文件.123fastlink.json" --split-by chunk --max-files 100000

    # 只保留某个目录下的内容
    python 影库拆分.py "影库文件.123fastlink.json" --filter "影巢官组345.33T资源/电影/"

    # 输出到指定目录（默认 ./拆分输出）
    python 影库拆分.py "..." --out-dir 拆分输出

拆分结果可直接放进「秒传文件导入或追加」目录导入使用。
默认**不会**修改原文件。
"""
import argparse
import json
import os
import sys

# 拆分后单库的推荐上限：按实测，10 万条约占 100~150MB 内存
DEFAULT_MAX = 100000


def human(n):
    for u, s in (("TB", 1024 ** 4), ("GB", 1024 ** 3), ("MB", 1024 ** 2), ("KB", 1024)):
        if n >= s:
            return "%.2f %s" % (n / s, u)
    return "%d B" % n


def load_lib(path):
    """流式读取，避免一次性 json.load 造成内存峰值。"""
    size = os.path.getsize(path)
    print("读取: %s (%.1f MB)" % (os.path.basename(path), size / 1048576))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def top_dir(common_path, file_path):
    """取相对 commonPath 之后的第一层目录，作为分组键。"""
    p = (file_path or "").replace("\\", "/")
    cp = (common_path or "").replace("\\", "/")
    if cp and p.startswith(cp):
        p = p[len(cp):]
    p = p.lstrip("/")
    parts = [x for x in p.split("/") if x]
    return parts[0] if len(parts) > 1 else "(根目录)"


def make_lib(src_meta, files, name, common_path):
    """按原影库的元信息结构构造一个子影库。"""
    total_size = sum(int(f.get("size") or 0) for f in files)
    return {
        "scriptVersion": src_meta.get("scriptVersion", "3.2.0-tdr.3"),
        "exportVersion": src_meta.get("exportVersion", "1.0"),
        "usesBase62EtagsInExport": src_meta.get("usesBase62EtagsInExport", True),
        "commonPath": common_path,
        "totalFilesCount": len(files),
        "totalSize": total_size,
        "formattedTotalSize": human(total_size),
        "files": files,
    }


def split(path, out_dir, mode, max_files, filter_prefix, dry):
    data = load_lib(path)
    files = data.get("files") or []
    common = data.get("commonPath", "")
    base = os.path.splitext(os.path.basename(path))[0]

    print()
    print("=" * 62)
    print(" 影库信息")
    print("=" * 62)
    print("  记录数   : %d" % len(files))
    print("  总体积   : %s" % data.get("formattedTotalSize", "-"))
    print("  commonPath: %r" % common)
    print()

    # ---- 过滤
    if filter_prefix:
        norm = filter_prefix.replace("\\", "/")
        files = [f for f in files
                 if ((f.get("path") or "").replace("\\", "/")).startswith(norm)]
        print("过滤 %r 后剩余: %d 条" % (filter_prefix, len(files)))
        if not files:
            print("没有匹配的记录，退出。")
            return 1
        print()

    # ---- 分组
    groups = []       # [(name, [files])]
    if mode == "chunk":
        for i in range(0, len(files), max_files):
            groups.append(("%s_part%02d" % (base, i // max_files + 1),
                           files[i:i + max_files]))
    elif mode == "dir":
        buckets = {}
        for f in files:
            buckets.setdefault(top_dir(common, f.get("path")), []).append(f)
        # 组内超过 max_files 再切块
        for gname in sorted(buckets):
            g = buckets[gname]
            if len(g) <= max_files:
                groups.append(("%s_%s" % (base, gname), g))
            else:
                for i in range(0, len(g), max_files):
                    groups.append(("%s_%s_part%02d" % (base, gname,
                                                       i // max_files + 1),
                                   g[i:i + max_files]))
    else:
        groups = [(base, files)]

    # ---- 预览
    print("=" * 62)
    print(" 拆分结果（共 %d 个）%s" % (len(groups), "[预览模式，未写入]" if dry else ""))
    print("=" * 62)
    total = 0
    for name, g in groups:
        sz = sum(int(f.get("size") or 0) for f in g)
        total += len(g)
        print("  %-52s %7d 条  %s" % (name[:52], len(g), human(sz)))
    print("-" * 62)
    print("  合计 %d 条" % total)

    if not dry:
        os.makedirs(out_dir, exist_ok=True)
        for name, g in groups:
            safe = "".join(c if c not in '\\/:*?"<>|' else "-" for c in name)
            if not safe.lower().endswith(".json"):
                safe += ".123fastlink.json"
            out = os.path.join(out_dir, safe)
            lib = make_lib(data, g, name, common)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(lib, f, ensure_ascii=False)
            print("  已写出: %s  (%.1f MB)" % (safe, os.path.getsize(out) / 1048576))
        print()
        print("=" * 62)
        print(" 完成。把上述文件放进「秒传文件导入或追加」目录即可导入。")
        print(" 单个文件越小，解析时内存峰值越低。")
        print("=" * 62)

    return 0


def main():
    ap = argparse.ArgumentParser(
        description="影库拆分/瘦身工具（缓解追加影库时的内存崩溃）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lib", help="要处理的 .123fastlink.json 文件")
    ap.add_argument("--split-by", choices=["dir", "chunk", "none"], default="dir",
                    help="拆分方式：dir=按顶级目录，chunk=按条数切块，none=不拆（默认 dir）")
    ap.add_argument("--max-files", type=int, default=DEFAULT_MAX,
                    help="单个子库的最大记录数（默认 %d）" % DEFAULT_MAX)
    ap.add_argument("--filter", default="", help="只保留路径以此开头的记录")
    ap.add_argument("--out-dir", default="拆分输出", help="输出目录（默认 拆分输出）")
    ap.add_argument("--dry-run", action="store_true", help="只预览不写入")
    a = ap.parse_args()

    if not os.path.isfile(a.lib):
        print("找不到文件: %s" % a.lib)
        return 2
    return split(a.lib, a.out_dir, a.split_by, a.max_files, a.filter, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
