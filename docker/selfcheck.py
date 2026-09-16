#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""镜像构建自检（无需 Docker）—— 源码版。

在没有 Docker 的机器上，把 Dockerfile 里除 `pip install` 与镜像打包之外的
每一步都真实跑一遍，提前暴露"构建时才炸"的问题：

  1. 构建上下文是否被 .dockerignore 正确裁剪（体积、必需文件都在）
  2. src/ 下 4 个模块 + 前端资源是否齐全
  3. 源码能否 compile（等同 Dockerfile 里的 compileall 步骤）
  4. 依赖是否可导入、4 个模块能否正常 import
  5. entry.py 能否在容器环境下把服务拉起来（真实起服务 + 探活）

用法:
    python docker/selfcheck.py            # 在项目根目录执行
    python docker/selfcheck.py --full     # 额外跑一遍真实启动探活
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
WORK = os.path.join(ROOT, ".selfcheck")

# Dockerfile 里 COPY 进镜像、因此**必须存在**的文件
REQUIRED = [
    "src/server.py",
    "src/pan123_api.py",
    "src/tasks.py",
    "src/library_store.py",
    "src/index.html",
    "src/style.css",
    "src/app.js",
    "src/bgm.mp3",
    "docker/entry.py",
]

# 前端资源（与源码同放 src/）
ASSETS = ["index.html", "style.css", "app.js", "bgm.mp3"]

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
            neg = r.startswith("!")
            if neg:
                r = r[1:]
            pat = r.replace("**/", "").replace("**", "*")
            if pat.startswith("*."):
                if name.lower().endswith(pat[1:].lower()):
                    hit, negated = True, neg
            elif pat == rel or pat == name or (parent and pat == parent):
                hit, negated = True, neg
            elif pat in rel.split(os.sep):
                hit, negated = True, neg
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

    # 源码版不再需要 exe，若仍传 exe 说明忽略规则没更新
    exes = [f for f, s in kept_files
            if f.lower().endswith(".exe") and s > 1048576]
    if exes:
        fail("上下文里仍有桌面版 exe（源码版镜像不需要，应排除）",
             "\n".join("%s (%.1f MB)" % (f, s / 1048576) for f, s in
                       [(f, dict(kept_files)[f]) for f in exes]))
    else:
        ok("已排除桌面版 exe（源码版镜像不需要）")

    big = [(f, s) for f, s in kept_files
           if s > 5 * 1048576 and f not in REQUIRED]
    if big:
        fail("上下文内仍有 >5MB 的冗余大文件（应排除）",
             "\n".join("%s (%.1f MB)" % (f, s / 1048576) for f, s in big))
    else:
        ok("上下文内无 >5MB 冗余大文件")


# ------------------------------------------------------- 2. 源码与资源
def check_sources():
    section("2. 源码与前端资源")
    mods = ["server.py", "pan123_api.py", "tasks.py", "library_store.py"]
    miss = [m for m in mods if not os.path.exists(os.path.join(SRC, m))]
    if miss:
        fail("缺少源码模块", ", ".join(miss))
    else:
        ok("4 个源码模块齐全: %s" % ", ".join(mods))

    miss = [a for a in ASSETS if not os.path.exists(os.path.join(SRC, a))]
    if miss:
        fail("缺少前端资源", ", ".join(miss))
    else:
        info = ", ".join("%s %d B" % (a, os.path.getsize(os.path.join(SRC, a)))
                         for a in ASSETS)
        ok("前端资源齐全: %s" % info)


# ------------------------------------------------------ 3. 编译（同 Dockerfile）
def check_compile():
    section("3. 源码编译（等同 Dockerfile 的 compileall 步骤）")
    bad = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".py"):
            continue
        p = os.path.join(SRC, fn)
        try:
            compile(open(p, encoding="utf-8").read(), p, "exec")
        except SyntaxError as e:
            bad.append("%s L%s: %s" % (fn, e.lineno, e.msg))
    if bad:
        fail("存在语法错误", "\n".join(bad))
    else:
        ok("全部 .py 编译通过")


# ------------------------------------------------------- 4. 依赖与导入
def check_imports():
    section("4. 依赖与模块导入")
    for mod in ("requests", "segno"):
        try:
            __import__(mod)
            ok("%s 已安装" % mod)
        except ImportError:
            print("  \033[93m[提示]\033[0m %s 本机未安装"
                  "（Dockerfile 中会 pip install，不影响镜像构建）" % mod)

    code = (
        "import sys; sys.path.insert(0, %r);"
        "import server, pan123_api, tasks, library_store as ls;"
        "print('OK', server.APP_VERSION, server.BASE_DIR)"
    ) % SRC
    proc = subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=ROOT)
    if proc.returncode == 0:
        ok("四模块导入成功: %s" % (proc.stdout or "").strip()[:90])
    else:
        fail("模块导入失败", (proc.stderr or "").strip()[-400:])


# ------------------------------------------------------------ 5. entry.py
def check_entry():
    section("5. 检查 entry.py（语法与关键适配逻辑）")
    p = os.path.join(ROOT, "docker", "entry.py")
    try:
        src = open(p, encoding="utf-8").read()
        compile(src, p, "exec")
        ok("语法检查通过")
    except Exception as e:
        fail("语法错误", e)
        return
    if "marshal.loads" not in src:
        ok("不再反序列化字节码（已改为导入源码）")
    else:
        fail("entry.py 仍在用 marshal.loads 加载字节码")
    for token, desc in [("server_bind", "监听地址改写为 0.0.0.0"),
                        ("webbrowser", "屏蔽浏览器拉起"),
                        ("LB_BROWSER", "跳过 pywebview 桌面壳"),
                        ("makedirs", "预建数据目录"),
                        ("import server", "导入源码模块")]:
        if token in src:
            ok("含适配逻辑: %s" % desc)
        else:
            fail("缺少适配逻辑: %s" % desc)


# ------------------------------------------------------- 6. 真实启动探活
def check_runtime():
    section("6. 真实启动探活（起服务 + 打接口）")
    data = os.path.join(WORK, "data")
    os.makedirs(data, exist_ok=True)
    code = r"""
import json, sys, threading, time, urllib.request
sys.path.insert(0, r'{src}')
sys.argv = ['server.py', '--dir=' + r'{data}']
import server
server.init_data_root()
threading.Thread(target=server.run_server, daemon=True).start()
time.sleep(2)
B = 'http://127.0.0.1:' + str(server.HTTP_PORT)
out = {}
for p in ('/api/ping', '/api/libs', '/api/login/status',
          '/', '/style.css', '/app.js', '/bgm.wav'):
    try:
        r = urllib.request.urlopen(B + p, timeout=20)
        out[p] = (r.status, len(r.read()))
    except Exception as e:
        out[p] = ('ERR', str(e)[:60])
print(json.dumps(out))
""".replace('{src}', SRC).replace('{data}', data)
    proc = subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=ROOT,
                          timeout=180)
    if proc.returncode != 0:
        fail("启动失败", (proc.stderr or "").strip()[-500:])
        return
    # 输出里可能混有子进程的日志行，取最后一行合法 JSON
    res = None
    for line in reversed((proc.stdout or "").strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except ValueError:
                continue
    if res is None:
        fail("无法解析探活结果", proc.stdout)
        return
    allok = True
    for p, v in res.items():
        if v[0] == 200:
            ok("%-22s HTTP 200  %6d B" % (p, v[1]))
        else:
            allok = False
            fail("%-22s %s" % (p, v))
    if allok:
        ok("接口与静态资源全部正常")


def main():
    print("=" * 64)
    print(" 123云盘影库搜索工具 —— 镜像构建自检（源码版，无需 Docker）")
    print("=" * 64)
    check_context()
    check_sources()
    check_compile()
    check_imports()
    check_entry()
    if "--full" in sys.argv or True:
        check_runtime()
    print("\n" + "=" * 64)
    print(" 结果：%d 项通过，%d 项失败" % (ok_count, fail_count))
    print("=" * 64)
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
