#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""123云盘影库搜索工具 —— 本地启动器（Windows / macOS / Linux 桌面）。

双击本文件即可在本机运行，自动打开浏览器。

与 docker/entry.py 的区别：
  entry.py    是给容器用的（监听 0.0.0.0、不拉浏览器、数据目录固定 /data）
  本文件      是给桌面用的（监听本机、自动开浏览器、数据目录在项目下的 data/）

用法：
    python run.py                  # 正常启动，自动开浏览器
    python run.py --dir D:\影库     # 换数据目录
    python run.py --no-browser     # 不自动开浏览器
    python run.py --check          # 只做环境自检，不启动

端口固定从 5890 起，被占用会自动往后找（不需要手动指定）。
"""
import argparse
import os
import sys
import threading
import time
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, 'src')
DEFAULT_DATA = os.path.join(HERE, 'data')


def info(msg):
    print('  %s' % msg, flush=True)


def head(msg):
    print()
    print('=' * 66)
    print('  %s' % msg)
    print('=' * 66)


def check_env():
    """环境自检，返回 (ok, 问题列表)。"""
    problems = []

    # Python 版本
    if sys.version_info < (3, 8):
        problems.append('Python 版本过低（需要 3.8+），当前 %s'
                        % sys.version.split()[0])

    # 依赖
    try:
        import requests  # noqa: F401
    except ImportError:
        problems.append('缺少依赖 requests，请运行：'
                        'pip install requests')

    # 源码
    for n in ('server.py', 'pan123_api.py', 'tasks.py', 'library_store.py'):
        if not os.path.isfile(os.path.join(SRC_DIR, n)):
            problems.append('缺少源码文件 src/%s' % n)

    # 前端资源
    for n in ('index.html', 'style.css', 'app.js'):
        if not os.path.isfile(os.path.join(SRC_DIR, n)):
            problems.append('缺少前端资源 src/%s' % n)

    return (not problems), problems


def show_data_summary(data_dir):
    """打印数据目录概况（不加载，只看文件大小）。"""
    imp = os.path.join(data_dir, '秒传文件导入或追加')
    if not os.path.isdir(imp):
        info('数据目录还没有影库（首次启动会自动创建子目录）')
        return
    names = [n for n in sorted(os.listdir(imp))
             if n.lower().endswith('.json') and not n.startswith('.')]
    if not names:
        info('数据目录还没有影库')
        return
    info('发现 %d 个影库：' % len(names))
    total = 0
    for n in names:
        sz = os.path.getsize(os.path.join(imp, n))
        total += sz
        peak = sz / 1048576 * 7.8
        flag = '⚠' if peak > 1000 else ' '
        info('  %s %-42s %7.1f MB  预估峰值 %5.0f MB'
             % (flag, n[:42], sz / 1048576, peak))
    info('  %s %-42s %7.1f MB  预估峰值 %5.0f MB'
         % (' ', '合计', total / 1048576, total / 1048576 * 7.8))
    if total / 1048576 * 7.8 > 1500:
        print()
        info('⚠ 影库较大，启动时加载需要约 %.0f 秒、内存约 %.0f MB'
             % (total / 1048576 * 0.065, total / 1048576 * 4.4))
        info('  若启动失败/闪退，用 python tools/mem_test.py --append 测内存')


def main():
    ap = argparse.ArgumentParser(description='123云盘影库搜索工具 · 本地启动器')
    ap.add_argument('--dir', default=DEFAULT_DATA, help='数据目录')
    ap.add_argument('--no-browser', action='store_true', help='不自动开浏览器')
    ap.add_argument('--check', action='store_true', help='只自检不启动')
    args = ap.parse_args()

    print()
    print('  123云盘影库搜索工具 —— 本地启动')
    print('  %s' % HERE)

    head('1. 环境自检')
    ok, problems = check_env()
    if not ok:
        for p in problems:
            print('  ✗ %s' % p)
        print()
        print('  自检未通过，请先解决上面的问题。')
        return 2
    info('✓ Python %s' % sys.version.split()[0])
    info('✓ 依赖齐全')
    info('✓ 源码与前端资源完整')

    head('2. 数据目录')
    data_dir = os.path.abspath(args.dir)
    info('路径: %s' % data_dir)
    os.makedirs(os.path.join(data_dir, '秒传文件导入或追加'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, '秒传文件导出'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, '记录数据存放目录【勿动】'), exist_ok=True)
    show_data_summary(data_dir)

    if args.check:
        head('自检完成')
        info('未启动服务（--check）')
        return 0

    head('3. 启动服务')
    sys.path.insert(0, SRC_DIR)

    # server.py 只认 --dir=；端口固定从 5890 起，被占用会自动往后找
    sys.argv = ['server.py', '--dir=' + data_dir]

    try:
        import server
    except Exception as e:
        print('  ✗ 导入 src/server.py 失败: %s' % e)
        import traceback
        traceback.print_exc()
        return 3

    info('正在加载影库…（影库大的话要等十几秒，请耐心）')
    t0 = time.time()
    try:
        server.init_data_root()
    except Exception as e:
        print('  ✗ 初始化失败: %s' % e)
        import traceback
        traceback.print_exc()
        return 4

    n = len(server.STORE.libraries) if server.STORE else 0
    total_files = sum(len(l.files) for l in server.STORE.libraries.values()) \
        if server.STORE else 0
    info('✓ 加载完成，耗时 %.1f 秒' % (time.time() - t0))
    info('✓ 影库 %d 个 / 文件 %d 条' % (n, total_files))

    url = 'http://127.0.0.1:%d/' % server.HTTP_PORT

    if not args.no_browser:
        def _open():
            time.sleep(1.2)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=_open, daemon=True).start()

    print()
    print('-' * 66)
    print('  访问地址 : %s' % url)
    print('  版本     : %s' % server.APP_VERSION)
    print('  数据目录 : %s' % data_dir)
    print('  停止服务 : 按 Ctrl+C')
    print('-' * 66)
    print()

    try:
        server.run_server()
    except KeyboardInterrupt:
        print()
        print('  已停止。')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
