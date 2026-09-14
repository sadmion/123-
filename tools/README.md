# 源码还原工具（CPython 3.13 反编译器）

从 `123云盘影库搜索工具.exe` 还原 Python 源码的工具集。

## 为什么需要自己写

现成反编译工具**全部不支持 Python 3.13**，而本 exe 恰由 3.13 打包：

| 工具 | 状况 |
|---|---|
| decompyle3 | ❌ 源码里 `PYTHON_VERSIONS = {(3,7),(3,8)}`，写死只支持 3.7/3.8 |
| uncompyle6 | ❌ 同上 |
| xdis 6.3.0 | ⚠️ 有 3.13 的 opcode 表，但没有语法重建器 |
| pycdc | ❌ 需 C++ 工具链；官方 release 产物已过期、需登录下载 |

因此本项目自建反编译器：`decompiler_313.py`（表达式还原）+ `build_src.py`（结构化）。

## 用法

```bash
# 1) 从 exe 抽出字节码
python ../docker/extract_pyinstaller.py "../123云盘影库搜索工具.exe" --linux -o bytecode

# 2) 反编译成源码
python build_src.py bytecode decompiled

# 3) 查看某个函数的结构（调试用）
python cf_313.py bytecode/server.pyc
```

## 文件说明

| 文件 | 作用 |
|---|---|
| `decompiler_313.py` | 表达式栈还原：把字节码指令还原成嵌套表达式；含函数/类签名还原 |
| `build_src.py` | 结构化还原主程序：在表达式基础上还原 if/for/while/try/with |
| `cf_313.py` | 控制流分析器（独立工具）：基本块划分、循环与异常作用域识别 |
| `bytecode/` | 从 exe 抽出的 4 个模块字节码（**还原的唯一依据，请保留**） |
| `decompiled/` | 反编译产出（需人工校对，见下） |

## 当前还原质量

| 模块 | 有效行数 | 干净行 | 覆盖率 |
|---|---|---|---|
| **server.py** | 3035 | 2755 | **90%** |
| **pan123_api.py** | 998 | 851 | **85%** |
| library_store.py | 1360 | 869 | 63% |
| tasks.py | 1270 | 961 | 75% |
| **合计** | 6663 | 5436 | **81%** |

**已可靠还原**：
- 全部导入语句、模块级常量（`APP_NAME` / `TMDB_KEY_DEFAULT` / `AUTH` / `BGM_MIME` 等）
- 全部函数与方法签名（参数名、默认值标志、`*args` / `**kwargs`）
- 类定义与继承（`class Handler(BaseHTTPRequestHandler)`）及**全部方法**（`do_GET`/`do_POST`/`_json`/`_static`/`_body`…）
- **嵌套闭包函数**（如 `load_auth` 内的 `_verify`）
- `with` 语句（含 `as` 变量，如 `with open(_auth_file(),'r',encoding='utf-8') as f:`）
- 单层 `if` / `for` / `while` 结构
- `try` / `except OSError` 等异常类型识别
- 大部分表达式（运算、调用、下标、切片 `BINARY_SLICE`、容器、f-string）

**尚不完整**（产出里以注释标注，绝不猜测）：
- 深度嵌套（>8 层）内部的结构（已做深度保护，退化为平铺而非无限缩进）
- 布尔短路表达式（`and`/`or` 跳转未合并）
- 复杂循环体内语句边界（`for` 体含 `try` 时可能提前截断）
- 默认参数的实际值（字节码只存"有默认值"标志）
- 生成器/异步函数（`yield` / `await` 语义未完整重建）

## 产出文件的正确用法

⚠️ **`decompiled/` 不能直接运行**，定位是"带标注的逻辑还原稿"：

- `# [控制流]` / `# [未实现]` 标注处逻辑未完整还原
- `<栈空>` 表示表达式栈错位，需对照字节码补齐
- **单层结构的函数质量很高，可直接阅读**；深层嵌套需人工校对

**用途**：
1. **读懂逻辑**（当前主要用途，效果良好）：查找某功能的实现、理解接口参数
2. **指导改前端**：明确前端调用了哪些接口
3. **人工补全**：以 `bytecode/` 为唯一权威依据逐函数校对，得到可运行源码

## 校验产出的方法

```bash
# 语法检查（列出问题行号）
python -c "compile(open('decompiled/server.py',encoding='utf-8').read(),'s','exec')"

# 对照字节码核对某函数（权威依据）
python cf_313.py bytecode/server.pyc | less
```

## 已修复的关键问题（供后续维护参考）

1. **`dis.get_instructions` 递归崩溃**：大函数（1800+ 条指令）会触发 `findlabels` 的 RecursionError。改用 `_unpack_opargs` 线性解析（注意 3.13 返回 **4 元组**）。
2. **`dis._parse_exception_table` 同样递归**：自实现 varint 解码。
3. **`LOAD_GLOBAL`/`LOAD_ATTR` 的 arg 带 flag 位**：须 `arg >> 1` 取索引。
4. **DEREF 类指令使用统一索引空间**：`MAKE_CELL arg=3` 时 `co_cellvars=('t',)` 只有一个元素，arg 需先减去 `len(co_varnames)` 再查。
5. **`with` 的 ctx 取值顺序**：必须先执行完 ctx 表达式再 `pop()`。
6. **`POP_JUMP_IF_FALSE` 条件不取反**：then 体是"条件为真"分支。
7. **异常表里 with 与 try 混用**：用 handler 处是否出现 `CHECK_EXC_MATCH` 区分（`kind="except"` / `"cleanup"`）。
8. **缩进爆炸**：嵌套过深时退化平铺（`MAX_INDENT=8`）。

## 后续可提升的方向

按性价比排序：

1. **布尔短路合并**：识别 `JUMP_IF_*_OR_POP` 模式 → `and` / `or`
2. **循环体边界修正**：`for` 体内含 `try` 时的截断问题
3. **默认参数还原**：跟踪模块级 `LOAD_CONST <默认值元组> | MAKE_FUNCTION | SET_FUNCTION_ATTRIBUTE 1`
4. **生成器/异步**：`RETURN_GENERATOR` / `SEND` / `YIELD_VALUE` 语义重建
5. **`library_store.py` 提升**：当前 63% 最低，含较多深层嵌套
