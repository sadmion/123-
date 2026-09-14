#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PyInstaller 单文件归档提取器（用于 Docker 构建阶段）。

把 Windows 版 PyInstaller onefile exe 拆成可直接被 CPython 3.13 执行的
纯字节码模块 + 静态资源，从而让同一个构建产物能在 Linux 容器里运行。

用法:
    python extract_pyinstaller.py <app.exe> [--list] [-o 输出目录]
"""
import argparse
import importlib.util
import marshal
import os
import struct
import sys
import zlib

COOKIE_MAGIC = b"MEI\014\013\012\013\016"
COOKIE_SIZE = 88          # magic(8) + 4*4 + pylibname(64)
TOC_ENTRY_HEADER = 18     # 4*4 + compressed_flag(1) + typecode(1)
PYC_MAGIC = importlib.util.MAGIC_NUMBER   # 当前解释器的 pyc 魔数


def parse_archive(blob):
    """解析 PyInstaller CArchive，返回 (cookie_info, entries)。

    注意：onefile 产物常带 overlay（引导器/附加数据在归档之前），
    归档内所有偏移都是相对 overlay 起点（= 文件长度 - 包长度）的，
    必须做换算，否则 TOC 会解析为空。
    """
    cookie_pos = blob.rfind(COOKIE_MAGIC)
    if cookie_pos < 0:
        raise SystemExit("未找到 PyInstaller 归档标记，可能不是 PyInstaller onefile 产物")
    cookie = blob[cookie_pos:cookie_pos + COOKIE_SIZE]
    _, pkg_len, toc_offset, toc_len, pyver, pylib = struct.unpack("!8sIIII64s", cookie)

    overlay = len(blob) - pkg_len          # 归档起点（引导器长度）
    toc_start = overlay + toc_offset

    pos = toc_start
    entries = []
    while pos < toc_start + toc_len:
        header = blob[pos:pos + TOC_ENTRY_HEADER]
        if len(header) < TOC_ENTRY_HEADER:
            break
        e_len, e_off, c_size, u_size, c_flag, t_code = struct.unpack("!IIIIBc", header)
        name = blob[pos + TOC_ENTRY_HEADER:pos + e_len].decode("utf-8", "replace").rstrip("\x00")
        entries.append({
            "name": name,
            "offset": overlay + e_off,
            "compressed_size": c_size,
            "uncompressed_size": u_size,
            "compressed": bool(c_flag),
            "typecode": t_code.decode("latin-1"),
        })
        pos += e_len

    info = {
        "package_length": pkg_len,
        "overlay": overlay,
        "toc_offset": toc_offset,
        "toc_length": toc_len,
        "python_version": pyver,
        "python_library": pylib.rstrip(b"\x00").decode("latin-1"),
    }
    return info, entries


def read_entry(blob, entry):
    raw = blob[entry["offset"]:entry["offset"] + entry["compressed_size"] or None]
    if entry["compressed"]:
        raw = zlib.decompress(raw)
    return raw


def write_pyc(path, payload, magic=PYC_MAGIC):
    """写出标准 sourceless pyc。

    payload 可能已带 pyc 头（PyInstaller 的 'm' 类条目），也可能只有裸
    marshal 字节码（'s' 类入口脚本与 PYZ 内的模块），这里统一处理。
    注意：必须用当前解释器的 magic 重写头部——exe 可能是 3.13 早期小版本
    编译的（magic 3531），容器里的 3.13.12 是 3571，照搬旧 magic 会
    直接 ImportError: bad magic number。
    """
    if payload[:4] == magic or payload[1:4] == b"\r\r\n":
        data = payload
    else:
        data = magic + b"\x00" * 12 + payload
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def extract_pyz(blob, entry, out_dir, verbose=True, allow=None):
    """展开 PYZ-00.pyz，把里面每个模块写成独立 .pyc。

    allow 为模块名白名单（None 表示展开全部非标准库模块）。
    """
    data = read_entry(blob, entry)
    if data[:4] != b"PYZ\0":
        raise SystemExit("PYZ 头异常: %r" % data[:8])
    magic = data[4:8]
    toc_offset = struct.unpack("!I", data[8:12])[0]
    toc = marshal.loads(data[toc_offset:])
    count = 0
    for item in toc:
        name, spec = item[0], item[1]
        if isinstance(name, bytes):
            name = name.decode("utf-8", "replace")
        typcd, mod_pos, mod_len = spec[0], spec[1], spec[2]
        if allow is not None and name.split(".")[0] not in allow:
            continue
        payload = data[mod_pos:mod_pos + mod_len]
        # PYZ 条目的压缩标记在不同 PyInstaller 版本里是 'zlib'/'raw' 或整数，
        # 直接用「试解压」判断，比匹配标记更可靠。
        try:
            payload = zlib.decompress(payload)
        except zlib.error:
            pass
        # 展开全部时过滤掉 stdlib：容器里用官方 Python 3.13 的更可靠
        if allow is None and (name.startswith(("_", "encodings", "importlib")) or "." in name):
            continue
        write_pyc(os.path.join(out_dir, name + ".pyc"), payload, magic)
        count += 1
        if verbose:
            print("    PYZ 模块 -> %s.pyc (%d B)" % (name, len(payload)))
    return count


# Linux 容器里需要的静态资源后缀（前端三件套 + 背景音乐 + 图标等）
DATA_EXTS = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".mp3", ".ogg", ".wav",
             ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".woff", ".woff2",
             ".ttf", ".pem", ".txt", ".csv", ".md"}
# 这些名字下的东西由镜像里的 pip 依赖提供，或属于 Windows 专有运行时
SKIP_PREFIX = ("clr_loader", "pythonnet", "cryptography", "bcrypt",
               "charset_normalizer", "certifi", "setuptools", "pip")
SKIP_NAMES = {"base_library.zip"}


def linux_filter(entry):
    """判断某个归档条目在 Linux 容器里是否需要保留。"""
    tc, name = entry["typecode"], entry["name"]
    if tc in ("s", "z"):
        # PyInstaller 的 Windows 运行时钩子/bootloader 在 Linux 下没有意义
        base = os.path.basename(name)
        return not base.startswith(("pyi_rth", "pyiboot"))
    if tc in ("m", "M"):          # pyimod0x 运行时钩子，容器里不需要
        return False
    if name in SKIP_NAMES or ".dist-info" in name:
        return False
    if name.split("\\")[0].split("/")[0] in SKIP_PREFIX:
        return False
    return os.path.splitext(name)[1].lower() in DATA_EXTS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe")
    ap.add_argument("-o", "--out", default="app")
    ap.add_argument("--list", action="store_true", help="只列出归档目录")
    ap.add_argument("--linux", action="store_true",
                    help="Linux 容器预设：丢弃 Windows 二进制，只留自有模块与静态资源")
    ap.add_argument("--modules", default="pan123_api,tasks,library_store",
                    help="从 PYZ 里展开的模块白名单（逗号分隔）")
    args = ap.parse_args()

    with open(args.exe, "rb") as f:
        blob = f.read()

    info, entries = parse_archive(blob)
    print("[*] 归档信息: python=%s  pylib=%s  overlay=%d  条目数=%d"
          % (info["python_version"], info["python_library"], info["overlay"], len(entries)))

    if args.list:
        print("%-4s %-42s %12s %12s" % ("code", "name", "stored", "raw"))
        for e in entries:
            print("%-4s %-42s %12d %12d"
                  % (e["typecode"], e["name"], e["compressed_size"], e["uncompressed_size"]))
        return

    allow = {m.strip() for m in args.modules.split(",") if m.strip()}
    os.makedirs(args.out, exist_ok=True)
    stat = {"pyz": 0, "script": 0, "data": 0, "skip": 0}
    for e in entries:
        tc, name = e["typecode"], e["name"]
        if args.linux and not linux_filter(e):
            stat["skip"] += 1
            continue
        if tc == "z":
            print("[*] 展开 PYZ: %s（白名单: %s）" % (name, ",".join(sorted(allow)) or "全部"))
            stat["pyz"] += extract_pyz(blob, e, args.out, allow=allow or None)
        elif tc in ("s", "m", "M"):
            write_pyc(os.path.join(args.out, name + ".pyc"), read_entry(blob, e))
            stat["script"] += 1
            print("[*] 脚本/模块: %s.pyc" % name)
        else:
            # 归档里是 Windows 相对路径（反斜杠），在 Linux 上必须换成
            # 真正的目录层级，否则会生成名字里带反斜杠的文件
            rel = name.replace("\\", "/").lstrip("/")
            dst = os.path.join(args.out, *rel.split("/"))
            os.makedirs(os.path.dirname(dst) or args.out, exist_ok=True)
            with open(dst, "wb") as f:
                f.write(read_entry(blob, e))
            stat["data"] += 1
            print("[*] 资源文件: %s (%d B)" % (rel, e["uncompressed_size"]))

    print("[+] 完成: PYZ 模块 %d 个, 脚本 %d 个, 资源 %d 个, 跳过 %d 个 -> %s"
          % (stat["pyz"], stat["script"], stat["data"], stat["skip"], args.out))


if __name__ == "__main__":
    main()
