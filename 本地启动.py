# -*- coding: utf-8 -*-
"""本地启动 —— 转发到 run.py。

保留这个中文文件名方便识别；真正的实现放在 run.py
（英文名可避免部分 Windows 环境的编码问题）。

你可以直接双击 run.py，效果完全一样。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

_target = os.path.join(HERE, 'run.py')
if not os.path.isfile(_target):
    print('找不到 run.py（应与本文件在同一目录）')
    sys.exit(2)

with open(_target, encoding='utf-8') as f:
    _code = f.read()

_g = {'__name__': '__main__', '__file__': _target}
exec(compile(_code, _target, 'exec'), _g)
