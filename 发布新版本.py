#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""版本发布工具 —— 改完源码后一键走完「自检 → 提交 → 打 tag → 触发镜像构建」

## 为什么需要它

Docker 部署采用「拉取 GHCR 镜像」方式，所以**版本更新的关键是让 CI 重建镜像**。
每次改完 src/ 下的源码后需要：改代码 → 自检 → 提交 → 打 tag 推送 → 等 CI 完成。
本脚本把这一串串起来，并做必要的前置校验。

## 用法

    # 1) 改好 src/ 下的源码（或替换前端资源），然后：

    # 查看当前状态，预演一遍（不提交）
    python 发布新版本.py --version 1.0.4 --note "修复xx" --dry-run

    # 正式发布
    python 发布新版本.py --version 1.0.4 --note "修复xx"

    # 只做自检，不发布
    python 发布新版本.py --check

## 它会做什么

1. 校验仓库状态（源码是否更新、是否在 git 仓库里）
2. 跑 docker/selfcheck.py（30 项构建自检，不需要 Docker）
3. git add/commit（规范化提交信息）
4. 打 tag 并推送（触发 GitHub Actions 重建镜像）
5. 打印后续步骤（等 CI、在服务器上 pull）

## 前置要求

- 已安装 git，且能推送到 origin
- 本机 Python 3.8+（跑自检用）
"""
import argparse
import os
import re
import subprocess
import sys
import time

SRC = "src"


def run(cmd, check=True, capture=True):
    r = subprocess.run(cmd, shell=True, capture_output=capture, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        out = (r.stdout or "") + (r.stderr or "")
        raise RuntimeError("命令失败: %s\n%s" % (cmd, out.strip()[:600]))
    return r


def out(cmd):
    return run(cmd).stdout.strip()


def step(n, total, title):
    print()
    print("\033[96m[%d/%d] %s\033[0m" % (n, total, title))


def ok(msg):
    print("  \033[92m✓\033[0m %s" % msg)


def warn(msg):
    print("  \033[93m!\033[0m %s" % msg)


def err(msg):
    print("  \033[91m✗\033[0m %s" % msg)


def main():
    ap = argparse.ArgumentParser(
        description="改完源码后一键发布新版本（触发镜像重建）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", help="版本号，如 1.0.4（会自动加 v 前缀）")
    ap.add_argument("--note", default="", help="更新说明")
    ap.add_argument("--check", action="store_true", help="只做自检")
    ap.add_argument("--dry-run", action="store_true", help="预演，不提交不推送")
    ap.add_argument("--skip-selfcheck", action="store_true", help="跳过构建自检")
    a = ap.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    T = 5

    print("=" * 64)
    print(" 版本发布工具")
    print("=" * 64)
    print("项目目录: %s" % root)

    # ---------- 1. 仓库与文件校验
    step(1, T, "校验仓库状态")
    if not os.path.isdir(".git"):
        err("不是 git 仓库")
        return 2
    ok("git 仓库正常")
    ok("当前分支: %s" % out("git rev-parse --abbrev-ref HEAD"))

    if not os.path.isdir(SRC):
        err("找不到源码目录 %s" % SRC)
        return 2
    mods = [f for f in sorted(os.listdir(SRC)) if f.endswith(".py")]
    ok("源码目录 %s（%d 个模块: %s）" % (SRC, len(mods), ", ".join(mods)))
    total = sum(os.path.getsize(os.path.join(SRC, f)) for f in os.listdir(SRC))
    ok("源码与资源合计 %.1f KB" % (total / 1024))

    # 源码是否被改动
    st = out("git status --porcelain -- \"%s\"" % SRC)
    src_changed = bool(st)
    if src_changed:
        ok("检测到源码有改动（将随本次提交一起推送）")
    else:
        warn("源码没有变化 —— 若你刚改过代码，请确认已保存且路径正确")

    remote = out("git remote get-url origin")
    ok("远程仓库: %s" % remote)

    if a.check:
        print()
        print("（--check 模式，仅做校验，不提交）")
        return 0

    # ---------- 2. 构建自检
    step(2, T, "构建自检（不需要 Docker）")
    if a.skip_selfcheck:
        warn("已跳过")
    else:
        # 用当前解释器跑自检，保证与发布脚本处于同一环境
        # （写死 "python" 可能落到未装依赖的解释器上）
        _py = '"%s"' % sys.executable
        r = run('%s docker/selfcheck.py' % _py, check=False)
        text = (r.stdout or "") + (r.stderr or "")
        m = re.search(r"结果：(\d+) 项通过，(\d+) 项失败", text)
        if m:
            passed, failed = int(m.group(1)), int(m.group(2))
            if failed == 0:
                ok("%d 项通过，0 项失败" % passed)
            else:
                err("%d 项通过，%d 项失败" % (passed, failed))
                print(text[-1200:])
                print()
                err("自检未通过，已中止发布。请先修复上面的问题。")
                return 1
        else:
            warn("无法解析自检输出，请人工确认：")
            print(text[-800:])

    # ---------- 3. 版本号
    step(3, T, "确认版本号")
    version = a.version
    if not version:
        # 尝试从上一个 tag 递增
        try:
            last = out("git describe --tags --abbrev=0")
            m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", last)
            if m:
                version = "%s.%s.%s" % (m.group(1), m.group(2), int(m.group(3)) + 1)
                warn("未指定 --version，基于 %s 推断为 %s" % (last, version))
        except Exception:
            pass
    if not version:
        err("请用 --version 指定版本号，例如 --version 1.0.4")
        return 2
    version = version.lstrip("vV")
    tag = "v" + version
    ok("版本号: %s（tag: %s）" % (version, tag))

    # 检查 tag 是否已存在
    existing = out("git tag -l \"%s\"" % tag)
    if existing:
        warn("tag %s 已存在" % tag)
        if not a.dry_run:
            err("请换一个版本号，或先删除旧 tag：git tag -d %s && git push origin --delete %s"
                % (tag, tag))
            return 2

    # ---------- 4. 提交
    step(4, T, "提交改动")
    changed = out("git status --porcelain")
    if not changed:
        warn("没有需要提交的改动")
    else:
        print("  待提交的文件:")
        for line in changed.splitlines()[:20]:
            print("    %s" % line[:100])
        if len(changed.splitlines()) > 20:
            print("    ... 共 %d 项" % len(changed.splitlines()))

        msg = "更新到 V%s%s" % (version, ("：" + a.note) if a.note else "")
        if a.dry_run:
            warn("[预演] 将执行: git commit -m \"%s\"" % msg)
        else:
            run("git add -A")
            run("git commit -q -m \"%s\"" % msg)
            ok("已提交: %s" % msg)

    # ---------- 5. 推送 + tag
    step(5, T, "推送并触发镜像构建")
    if a.dry_run:
        warn("[预演] 将执行:")
        print("    git push origin HEAD")
        print("    git tag -a %s -m \"...\"" % tag)
        print("    git push origin %s" % tag)
    else:
        r = run("git push origin HEAD", check=False)
        if r.returncode != 0:
            err("推送失败：")
            print(((r.stdout or "") + (r.stderr or ""))[-600:])
            return 1
        ok("代码已推送")

        r = run("git tag -a %s -m \"发布 V%s\"" % (tag, version), check=False)
        if r.returncode != 0:
            err("打 tag 失败")
            return 1
        r = run("git push origin %s" % tag, check=False)
        if r.returncode != 0:
            err("tag 推送失败")
            return 1
        ok("tag %s 已推送 —— GitHub Actions 开始构建镜像" % tag)

    # ---------- 收尾
    print()
    print("=" * 64)
    if a.dry_run:
        print(" 预演完成，未做任何实际改动。去掉 --dry-run 即可正式发布。")
    else:
        print(" 已触发构建。接下来：")
        print()
        print("  1) 等镜像构建完成（约 1~3 分钟）")
        print("     查看进度: https://github.com/sadmion/123-/actions")
        print()
        print("  2) 构建变绿后，在你的 NAS 上更新：")
        print("     docker compose pull && docker compose up -d")
        print()
        print("  3) 验证：")
        print("     curl http://127.0.0.1:5890/api/login/status")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
