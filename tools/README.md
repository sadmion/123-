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

| 模块 | 行数 | 无噪音行 | 覆盖度 |
|---|---|---|---|
| server.py | 1620 | 1147 | ~70% |
| pan123_api.py | 1767 | 1423 | ~80% |
| library_store.py | 445 | 316 | ~71% |
| tasks.py | 123 | 81 | ~65% |

**已可靠还原**：
- 全部导入语句、模块级常量（`APP_NAME` / `TMDB_KEY_DEFAULT` / `AUTH` 结构等）
- 全部函数签名（含参数名、默认值来源、`*args` / `**kwargs`）
- 类定义与继承关系（如 `class Handler(BaseHTTPRequestHandler)`）
- 单层 `if` / `for` / `while` / `with` 结构
- 大部分表达式（运算、调用、下标、容器构建、f-string 拼装）

**尚不完整**（产出里以注释标注）：
- `try/except` 块边界（3.13 用异常表实现，与 `with` 共用机制，边界易错位）
- 嵌套多层循环内的变量绑定（`UNPACK_SEQUENCE`、复合 `LOAD_FAST_LOAD_FAST`）
- 复杂布尔短路表达式的跳转合并
- 默认参数值（字节码里只存"有默认值"的标志，实际值在模块级初始化时压栈）

## 产出文件的正确用法

⚠️ **`decompiled/` 里的代码不能直接运行**，它是"带注释的逻辑还原稿"：

- 标注 `# [控制流]` / `# [未实现]` 的行表示此处逻辑未完整还原
- 标注 `<栈空>` 的位置表示表达式栈在该处错位，需对照字节码人工补齐
- 缩进与结构大体正确，可直接阅读理解业务逻辑

**用途**：
1. **读懂逻辑**：定位某功能怎么实现的（这是当前主要用途，效果良好）
2. **指导改前端**：理解前端调了哪些接口、参数是什么
3. **人工补全**：以 `bytecode/` 为唯一权威依据，逐函数校对补齐，最终得到可运行源码

## 校验产出的方法

```bash
# 语法检查（会列出问题行号）
python -c "compile(open('decompiled/server.py',encoding='utf-8').read(),'s','exec')"

# 对照字节码核对某一函数（推荐，权威依据）
python cf_313.py bytecode/server.pyc | less
```

## 后续可提升的方向

若需进一步提高还原度，按性价比排序：

1. **修 try/except 边界**：区分"with 的异常表条目"与"真正的 try"，用 `depth` 字段判定
2. **补复合指令**：`UNPACK_SEQUENCE`、`STORE_FAST_STORE_FAST`、`LOAD_FAST_LOAD_FAST`（3.13 新增，用于加速）
3. **布尔短路还原**：识别 `JUMP_IF_*_OR_POP` 模式，合并成 `and` / `or`
4. **默认参数还原**：跟踪模块级 `LOAD_CONST <默认值元组> | MAKE_FUNCTION | SET_FUNCTION_ATTRIBUTE 1`
5. **栈对齐修复**：遇到未实现指令时按语义正确调整栈深（当前用占位符会累积偏移）

其中第 1、2 项收益最大。
