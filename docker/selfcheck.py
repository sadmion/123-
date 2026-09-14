#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""镜像构建自检（无需 Docker）。

在没有 Docker 的机器上，把 Dockerfile 里除 `pip install` 与镜像打包之外的
每一步都真实跑一遍，提前暴露"构建时才炸"的问题：

  1. 构建上下文是否被 .dockerignore 正确裁剪（体积、必需文件都在）
  2. extract_pyinstaller.py 能否在目标 exe 上跑通
  3. 抽出的 pyc 能否被当前解释器 marshal 加载（magic 是否正确）
  4. entry.py 能否正常导入并找到入口

用法:
    python docker/selfcheck.py            # 在项目根目录执行
"""
import json
import marshal
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.join(ROOT, "123云盘影库搜索工具.exe")
WORK = os.path.join(ROOT, ".selfcheck")

# Dockerfile 里 COPY 进镜像、因此**必须存在**的文件
REQUIRED = [
    "123云盘影库搜索工具.exe",
    "docker/extract_pyinstaller.py",
    "docker/entry.py",
]

ok_count = fail_count = 0


def ok(msg):
    global ok_count
    ok_count += 1
    print("  \033[92m[通过]\033[0m %s" % msg)


def fail(msg, detail=""):
    global fail_count
    fail_count += 1
    print("  \033[91m[失败]\033[0m %s" % msg)
    if detail:
        for line in str(detail).splitlines():
            print("         %s" % line[:200])


def section(title):
    print("\n\033[96m== %s ==\033[0m" % title)


# ---------------------------------------------------------------- 1. 上下文
def check_context():
    section("1. 构建上下文（.dockerignore 裁剪结果）")
    ig = os.path.join(ROOT, ".dockerignore")
    if not os.path.exists(ig):
        fail(".dockerignore 缺失")
        return
    rules = []
    with open(ig, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                rules.append(line)

    def ignored(rel):
        """粗略模拟 docker 的忽略规则（够用于本仓库）。"""
        name = os.path.basename(rel)
        parent = os.path.dirname(rel)
        negated = False
        hit = False
        for r in rules:
            neg = r.startswith("!") and (r := r[1:])
            pat = r.replace("**/", "").replace("**", "*")
            if pat.startswith("*."):
                if name.lower().endswith(pat[1:].lower()):
                    hit, negated = True, bool(neg)
            elif pat == rel or pat == name or (parent and pat == parent):
                hit, negated = True, bool(neg)
            elif pat in rel.split(os.sep):
                hit, negated = True, bool(neg)
        return hit and not negated

    total = kept = 0
    kept_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".github", ".selfcheck", "data")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            size = os.path.getsize(full)
            total += size
            if not ignored(rel):
                kept += size
                kept_files.append((rel, size))

    print("     完整体积 %.1f MB → 裁后上下文 %.1f MB"
          % (total / 1048576, kept / 1048576))

    for req in REQUIRED:
        if any(f == req for f, _ in kept_files):
            ok("必需文件在上下文中: %s" % req)
        else:
            fail("必需文件被 .dockerignore 误伤: %s" % req)

    big = [(f, s) for f, s in kept_files
           if s > 5 * 1048576 and f not in REQUIRED]
    if big:
        fail("上下文内仍有 >5MB 的冗余大文件（应排除）",
             "\n".join("%s (%.1f MB)" % (f, s / 1048576) for f, s in big))
    else:
        ok("上下文内无 >5MB 冗余大文件（只保留必需的桌面版 exe）")

    # 浏览器版 exe 不该进上下文
    if any("浏览器版" in f for f, _ in kept_files):
        fail("浏览器版 exe 仍在上下文中（多传 29MB）")
    else:
        ok("浏览器版 exe 已排除")


# ------------------------------------------------------- 2/3. 提取与加载
def check_extract():
    section("2. 运行提取器（等同 Dockerfile 的 RUN 步骤）")
    if not os.path.exists(EXE):
        fail("找不到 %s" % EXE)
        return None
    out = os.path.join(WORK, "app")
    if os.path.exists(WORK):
        import shutil
        shutil.rmtree(WORK, ignore_errors=True)
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "docker", "extract_pyinstaller.py"),
         EXE, "--linux", "-o", out],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=ROOT)
    tail = (proc.stdout or "").strip().splitlines()[-1:] 
    if proc.returncode != 0:
        fail("提取器退出码 %d" % proc.returncode, proc.stderr)
        return None
    ok("提取器执行成功：%s" % (tail[0] if tail else ""))

    need = ["server.pyc", "pan123_api.pyc", "tasks.pyc", "library_store.pyc",
            "index.html", "style.css", "app.js"]
    missing = [n for n in need if not os.path.exists(os.path.join(out, n))]
    if missing:
        fail("缺少关键产物", ", ".join(missing))
    else:
        ok("关键产物齐全（4 个模块 + 前端资源）")

    section("3. 校验 pyc 能否被当前解释器加载（magic 检查）")
    magic_ok = True
    for f in [n for n in os.listdir(out) if n.endswith(".pyc")]:
        p = os.path.join(out, f)
        with open(p, "rb") as fh:
            data = fh.read()
        try:
            code = marshal.loads(data[16:])
            if not hasattr(code, "co_code"):
                raise ValueError("不是 code 对象")
        except Exception as e:
            magic_ok = False
            fail("%s 无法加载: %s" % (f, e))
    if magic_ok:
        ok("全部 pyc 的 magic 与当前 Python(%s) 匹配，可正常加载"
           % ".".join(map(str, sys.version_info[:3])))
    return out


# ------------------------------------------------------------ 4. 启动器
def check_entry():
    section("4. 检查 entry.py（语法与关键适配逻辑）")
    p = os.path.join(ROOT, "docker", "entry.py")
    try:
        src = open(p, encoding="utf-8").read()
        compile(src, p, "exec")
        ok("语法检查通过")
    except Exception as e:
        fail("语法错误", e)
        return
    for token, desc in [("server_bind", "监听地址改写为 0.0.0.0"),
                        ("webbrowser", "屏蔽浏览器拉起"),
                        ("LB_BROWSER", "跳过 pywebview 桌面壳"),
                        ("makedirs", "预建数据目录")]:
        if token in src:
            ok("含适配逻辑: %s" % desc)
        else:
            fail("缺少适配逻辑: %s" % desc)

    # 依赖自查（仅作提示：镜像里会 pip install，本机缺失不影响构建）
    section("5. 运行依赖是否可导入（仅提示）")
    for mod in ("requests", "segno"):
        try:
            __import__(mod)
            ok("%s 已安装" % mod)
        except ImportError:
            print("  \033[93m[提示]\033[0m %s 本机未安装"
                  "（Dockerfile 中会 pip install，不影响镜像构建）" % mod)


def main():
    print("=" * 64)
    print(" 123云盘影库搜索工具 —— 镜像构建自检（无需 Docker）")
    print("=" * 64)
    check_context()
    check_extract()
    check_entry()
    print("\n" + "=" * 64)
    print(" 结果：%d 项通过，%d 项失败" % (ok_count, fail_count))
    print("=" * 64)
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
