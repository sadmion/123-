#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""启动修复 / 自检脚本

用途：当双击 exe「没反应、浏览器打不开」时，先跑一次这个脚本。

最常见的原因（本工具特有）：
    程序启动时要读 %APPDATA%/123云盘影库搜索工具/data_config.json 里的
    data_root；如果该目录**不存在**，它会尝试弹出图形化的目录选择框；
    在无 GUI 或弹窗失败的情况下就直接打印「未选择数据目录, 退出」并退出，
    表现就是"双击了但什么都没发生"。

本脚本会：
    1) 检查并创建数据目录（含三个必需子目录）
    2) 修正 data_config.json 指向正确路径
    3) 报告 5890 端口与配置状态

用法：
    python 启动修复.py            # 在项目根目录执行
    python 启动修复.py --check    # 只检查不修改
"""
import json
import os
import shutil
import socket
import sys

APP_NAME = "123云盘影库搜索工具"
PORT = 5890
SUBDIRS = ["秒传文件导入或追加", "秒传文件导出", "记录数据存放目录【勿动】"]


def appdata_dir():
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, APP_NAME)


def config_path():
    return os.path.join(appdata_dir(), "data_config.json")


def port_busy(port=PORT):
    """检测端口是否已被占用（说明服务已在运行）。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def main():
    check_only = "--check" in sys.argv
    root = os.path.dirname(os.path.abspath(__file__))
    data_root = os.path.join(root, "data")

    print("=" * 60)
    print(" %s —— 启动自检" % APP_NAME)
    print("=" * 60)
    print("项目目录 : %s" % root)
    print("目标数据目录: %s" % data_root)
    print("配置文件 : %s" % config_path())
    print()

    problems = []

    # ---- 1. 服务是否已在运行
    if port_busy():
        print("[提示] 端口 %d 已在监听 —— 服务应该已经启动了。" % PORT)
        print("       请直接打开浏览器访问：http://127.0.0.1:%d/" % PORT)
    else:
        print("[信息] 端口 %d 未监听（服务未运行）" % PORT)

    # ---- 2. 数据目录
    if os.path.isdir(data_root):
        print("[通过] 数据目录存在")
    else:
        problems.append("数据目录不存在")
        print("[问题] 数据目录不存在：%s" % data_root)
        if not check_only:
            os.makedirs(data_root, exist_ok=True)
            print("       → 已创建")

    if not check_only:
        for sub in SUBDIRS:
            p = os.path.join(data_root, sub)
            if not os.path.isdir(p):
                os.makedirs(p, exist_ok=True)
                print("[修复] 已创建子目录: %s" % sub)
        print("[通过] 三个子目录齐备")

    # ---- 3. 配置指向
    cfg_p = config_path()
    cur = None
    if os.path.isfile(cfg_p):
        try:
            cur = json.load(open(cfg_p, encoding="utf-8")).get("data_root")
        except Exception as e:
            print("[问题] 配置文件解析失败: %s" % e)
    else:
        print("[问题] 配置文件不存在（程序尚未成功启动过）")

    print("[信息] 配置里的 data_root = %r" % cur)

    need_fix = True
    if cur:
        norm = lambda x: os.path.normcase(os.path.normpath(x))
        if norm(cur) == norm(data_root) and os.path.isdir(cur):
            need_fix = False
            print("[通过] 配置指向正确且目录存在")

    if need_fix:
        problems.append("配置指向无效路径")
        if cur:
            print("[问题] 该路径不存在或不是当前项目的数据目录")
            print("       （常见于：之前用过其他目录，后来那个目录被删了）")
        if not check_only:
            os.makedirs(appdata_dir(), exist_ok=True)
            if os.path.isfile(cfg_p):
                shutil.copy(cfg_p, cfg_p + ".bak2")
            json.dump({"data_root": data_root},
                      open(cfg_p, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            print("[修复] 已将 data_root 修正为: %s" % data_root)

    # ---- 结论
    print()
    print("=" * 60)
    if not problems:
        print(" 检查通过，可以正常启动。")
        print(" 运行方式：双击 123云盘影库搜索工具.exe（或浏览器版）")
        print(" 然后访问 http://127.0.0.1:%d/" % PORT)
    elif check_only:
        print(" 发现问题（未修改）：%s" % "、".join(problems))
        print(" 去掉 --check 参数重新运行即可自动修复。")
    else:
        print(" 已自动修复。请重新双击 exe 启动。")
        print(" 若仍打不开，请看 data/logs/server.log 里的报错。")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
