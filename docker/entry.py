#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""123云盘影库搜索工具 —— 容器启动器（Linux / Docker，源码版）。

与旧版的区别：旧版需要先从桌面版 exe 里抽出 server.pyc 再用 marshal 反序列化
加载字节码，绕开 PyInstaller 引导器；现在直接导入项目 src/ 下的源码，
不再依赖桌面版 exe，改代码后重新构建镜像即可生效。

三项容器适配：
1. 监听地址：程序内部绑定 127.0.0.1，容器外无法访问 → 改写为 0.0.0.0
2. 桌面壳：容器无 GUI，屏蔽 pywebview 窗口与 webbrowser 拉起，改为打印地址
3. 数据目录：程序要求目录**必须已存在**（否则转去弹 tkinter 选择框并退出），
   这里提前创建，并通过 --dir= 传入（优先于 data_config.json 里的记录）
"""
import os
import socketserver
import sys
import webbrowser

APP_DIR = os.path.abspath(os.environ.get("APP_DIR", "/app"))
SRC_DIR = os.path.join(APP_DIR, "src")
DATA_DIR = os.path.abspath(os.environ.get("LB_DATA_ROOT", "/data"))
ENTRY = os.path.join(SRC_DIR, "server.py")
ACCESS_PORT = os.environ.get("LB_PORT", "5890")


def log(msg):
    print("[entry] %s" % msg, flush=True)


# ---------- 适配 1: 监听 0.0.0.0 ----------
_orig_server_bind = socketserver.TCPServer.server_bind


def _server_bind(self):
    addr = self.server_address
    if addr and addr[0] in ("127.0.0.1", "localhost", "::1"):
        self.server_address = ("0.0.0.0",) + tuple(addr[1:])
        log("监听地址改写: %s:%s -> 0.0.0.0:%s" % (addr[0], addr[1], addr[1]))
    return _orig_server_bind(self)


socketserver.TCPServer.server_bind = _server_bind


# ---------- 适配 2: 无浏览器环境（不拉起桌面窗口/浏览器） ----------
def _no_browser(url=None, *args, **kwargs):
    log("容器内不拉起浏览器，请在宿主机访问: http://localhost:%s/" % ACCESS_PORT)
    return False


for _name in ("open", "open_new", "open_new_tab"):
    setattr(webbrowser, _name, _no_browser)


def main():
    # ---------- 适配 3: 数据目录 ----------
    os.makedirs(DATA_DIR, exist_ok=True)
    os.environ.setdefault("LB_BROWSER", "1")   # 跳过 pywebview 桌面窗口分支

    if not os.path.exists(ENTRY):
        log("找不到 %s，请确认镜像里已包含 src/ 源码目录" % ENTRY)
        return 2

    sys.path.insert(0, SRC_DIR)
    # 去掉外部传入的 --dir=，强制使用容器数据目录
    argv = [a for a in sys.argv[1:] if not a.startswith("--dir=")]
    sys.argv = ["server.py", "--dir=" + DATA_DIR] + argv
    log("APP_DIR=%s  SRC_DIR=%s  DATA_DIR=%s" % (APP_DIR, SRC_DIR, DATA_DIR))

    import server
    # server.py 的 BASE_DIR 由 __file__ 推导，即 src/ 目录，
    # 前端静态资源（index.html / app.js / style.css）与源码同放在 src/。
    log("静态资源目录: %s" % server.BASE_DIR)
    server.init_data_root()
    log("数据目录就绪，服务启动中…")
    server.run_server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
