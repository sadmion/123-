#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""断点文件修复工具 —— 解决「提取失败: 'skipped'」

## 问题

程序在「分享链接提取」时支持断点续传，断点文件位于：

    <数据目录>/_checkpoints/extract_<分享key>.json

恢复提取时，代码这样读取：

    scanned = resume_offset['scanned']
    skipped = resume_offset['skipped']        # ← 硬下标，缺键就 KeyError
    done_dirs = set(resume_offset.get('done_dirs') or [])   # 这个做了兼容

注意**不对称**：`done_dirs` 用了 `.get()`，但 `skipped` 用硬下标。

**如果断点文件是旧版本程序写的**（没有 `skipped` 字段），恢复时就会抛
`KeyError: 'skipped'`，前端显示「提取失败: 'skipped'」。

## 本工具做什么

扫描断点目录，补齐缺失字段（`scanned` / `skipped` / `done_dirs` /
`shareKey` / `total_files` / `file_filters` / `ts`），使旧断点可被新版本读取。

也支持直接删除断点（重新开始提取）。

## 用法

    # 查看所有断点（不修改）
    python 断点修复.py --list

    # 修复（补齐缺失字段，原文件备份为 .bak）
    python 断点修复.py --fix

    # 删除全部断点（重新开始提取）
    python 断点修复.py --clear

    # 指定数据目录
    python 断点修复.py --list --data-root "D:/123data"
"""
import argparse
import glob
import json
import os
import shutil
import sys

# 新版代码期望的字段（从 tasks.ExtractTask._save_checkpoint 还原）
REQUIRED = {
    "shareKey": "",
    "total_files": 0,
    "scanned": 0,
    "skipped": 0,
    "done_dirs": [],
    "file_filters": None,
    "ts": 0,
}


def find_data_root(explicit=None):
    """定位数据目录：优先命令行，其次程序配置，最后项目 data/。"""
    if explicit:
        return explicit
    # 1) 读程序配置
    cfg = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")),
                       "123云盘影库搜索工具", "data_config.json")
    if os.path.isfile(cfg):
        try:
            r = json.load(open(cfg, encoding="utf-8")).get("data_root")
            if r and os.path.isdir(r):
                return r
        except Exception:
            pass
    # 2) 项目内 data/
    here = os.path.dirname(os.path.abspath(__file__))
    cand = os.path.join(here, "data")
    if os.path.isdir(cand):
        return cand
    return None


def ck_dir(data_root):
    return os.path.join(data_root, "_checkpoints")


def list_ck(d):
    return sorted(glob.glob(os.path.join(d, "extract_*.json")))


def show(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print("    读取失败: %s" % e)
        return None
    if not isinstance(d, dict):
        print("    内容不是对象（可能是文件列表）")
        return None
    miss = [k for k in REQUIRED if k not in d]
    print("    shareKey   : %r" % d.get("shareKey"))
    print("    total_files: %s   scanned: %s   skipped: %s"
          % (d.get("total_files"), d.get("scanned"), d.get("skipped")))
    print("    done_dirs  : %s 个" % len(d.get("done_dirs") or []))
    print("    ts         : %s" % d.get("ts"))
    if miss:
        print("    ⚠ 缺失字段: %s   ← 会导致 KeyError" % ", ".join(miss))
    else:
        print("    字段完整")
    return d


def cmd_list(d, args):
    files = list_ck(d)
    print("断点目录: %s" % d)
    if not files:
        print("  （无断点文件）")
        return 0
    print("断点文件: %d 个" % len(files))
    for p in files:
        print()
        print("  %s" % os.path.basename(p))
        show(p)
    return 0


def cmd_fix(d, args):
    files = list_ck(d)
    if not files:
        print("无断点文件，无需修复。")
        return 0
    fixed = 0
    for p in files:
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("%s 读取失败: %s" % (os.path.basename(p), e))
            continue
        if not isinstance(data, dict):
            print("%s 不是对象，跳过（可能是已完成的结果文件列表）"
                  % os.path.basename(p))
            continue
        miss = [k for k in REQUIRED if k not in data]
        if not miss:
            print("%s 字段完整，跳过" % os.path.basename(p))
            continue
        # 备份
        if not os.path.isfile(p + ".bak"):
            shutil.copy(p, p + ".bak")
        for k in miss:
            v = REQUIRED[k]
            # done_dirs 若不存在，尝试从旧字段推断
            if k == "done_dirs":
                v = data.get("doneDirs") or data.get("dirs") or []
            data[k] = v
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("%s 已补齐: %s" % (os.path.basename(p), ", ".join(miss)))
        fixed += 1
    print()
    print("修复完成：%d 个文件" % fixed)
    if fixed:
        print("原文件已备份为 *.bak，可重新发起提取。")
    return 0


def cmd_clear(d, args):
    files = list_ck(d)
    if not files:
        print("无断点文件。")
        return 0
    print("将删除以下断点文件：")
    for p in files:
        print("  %s" % os.path.basename(p))
    if not args.yes:
        print()
        print("确认请加 --yes 参数重新执行。")
        return 0
    n = 0
    for p in files:
        try:
            os.remove(p)
            n += 1
        except Exception as e:
            print("  删除失败 %s: %s" % (os.path.basename(p), e))
    print("已删除 %d 个断点文件。" % n)
    print("现在可以重新发起提取。")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="断点文件修复（解决「提取失败: 'skipped'」）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", help="数据目录（默认自动探测）")
    ap.add_argument("--list", action="store_true", help="查看断点")
    ap.add_argument("--fix", action="store_true", help="补齐缺失字段")
    ap.add_argument("--clear", action="store_true", help="删除全部断点")
    ap.add_argument("--yes", action="store_true", help="--clear 时确认")
    a = ap.parse_args()

    root = find_data_root(a.data_root)
    if not root or not os.path.isdir(root):
        print("找不到数据目录。请用 --data-root 指定，例如：")
        print('  python 断点修复.py --list --data-root "D:/123data"')
        return 2
    d = ck_dir(root)
    os.makedirs(d, exist_ok=True)

    if a.fix:
        return cmd_fix(d, a)
    if a.clear:
        return cmd_clear(d, a)
    return cmd_list(d, a)


if __name__ == "__main__":
    sys.exit(main())
