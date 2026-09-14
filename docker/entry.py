#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""123云盘影库搜索工具 —— 容器启动器（Linux / Docker）。

Windows 版是 PyInstaller 打包产物，Linux 容器里没有对应的引导器，
因此这里直接加载构建阶段从 exe 抽出的字节码（server.pyc 等），
并做三项容器适配：

1. 监听地址：程序内部绑定 127.0.0.1，容器外无法访问 → 改写为 0.0.0.0
2. 桌面壳：容器无 GUI，屏蔽 pywebview 窗口与 webbrowser 拉起，改为打印地址
3. 数据目录：程序要求目录**必须已存在**（否则转去弹 tkinter 选择框并退出），
   这里提前创建，并通过 --dir= 传入（优先于 data_config.json 里的记录）
"""
import marshal
import os
import socketserver
import sys
import types
import webbrowser

APP_DIR = os.path.abspath(os.environ.get("APP_DIR", "/app"))
DATA_DIR = os.path.abspath(os.environ.get("LB_DATA_ROOT", "/data"))
ENTRY = os.path.join(APP_DIR, "server.pyc")
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
        log("找不到 %s，请确认镜像构建阶段执行过 extract_pyinstaller.py" % ENTRY)
        return 2

    sys.path.insert(0, APP_DIR)
    argv = [a for a in sys.argv[1:] if not a.startswith("--dir=")]
    sys.argv = ["server.py", "--dir=" + DATA_DIR] + argv
    log("APP_DIR=%s  DATA_DIR=%s" % (APP_DIR, DATA_DIR))

    with open(ENTRY, "rb") as f:
        code = marshal.loads(f.read()[16:])   # 跳过 16 字节 pyc 头

    module = types.ModuleType("__main__")
    module.__file__ = os.path.join(APP_DIR, "server.py")
    module.__builtins__ = __builtins__
    module.__loader__ = None
    module.__spec__ = None
    module.__package__ = None
    sys.modules["__main__"] = module

    exec(code, module.__dict__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
