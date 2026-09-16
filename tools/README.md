# tools/ —— 校验与运维工具

本目录三个工具：

| 工具 | 用途 |
|---|---|
| `verify_src.py` | 源码还原校验（比对字节码） |
| `mem_test.py` | 影库内存测试（诊断「追加影库崩溃」） |
| `split_library.py` | 影库拆分（降低加载峰值） |

---

# 一、verify_src.py —— 源码还原校验器

## 它解决什么问题

本项目的 `src/` 源码是从桌面版 exe 的字节码**逐函数手工还原**出来的
（现成反编译工具 `decompyle3` / `uncompyle6` 均不支持 Python 3.13）。

手工还原最大的风险是「**写错但不报错**」——程序能跑，行为却不对。例如：

- 把 `return` 写成 `break` → 遍历目录时遇到分页会**静默丢数据**
- 把嵌套 `if` 写成 `or` 短路 → 求值顺序变了，边界行为不同
- 漏掉内层 `try/except` → 出错时不再降级，直接抛异常

这些错误没有语法错误、没有运行时报错，**只能靠机械比对发现**。

## 原理

把还原出的源码编译成字节码，与原始 `.pyc` 里的对应函数逐个比对：

| 比对项 | 能抓到什么 |
|---|---|
| 函数清单 | 漏写的函数、多写的函数 |
| 字面量集合 | 字符串/数字常量抄错、漏写 |
| 参数名、局部变量名 | 变量漏声明、命名不一致 |
| 属性/方法名 | 调用错方法、漏调用 |
| 跳转指令分布 | `if`/`for`/`while`/`try` 的结构差异 |
| 指令规模偏离度 | 整段逻辑缺失或多余 |
| 闭包结构 | `cellvars`/`freevars` 丢失（闭包变量被错误外提） |

已过滤的噪音（不构成语义问题）：类体的 `__firstlineno__` 行号常量、
编译器注入的属性名、Python 3.12+ 零参 `super()` 编入的类名。

## 用法

```bash
# 校验单个模块
python tools/verify_src.py server

# 校验全部四个模块
python tools/verify_src.py --all

# 打印差异明细
python tools/verify_src.py server --detail
```

需要 `tools/bytecode/*.pyc` 存在（原始字节码，已从仓库移除，需另行准备）。

## 如何理解「一致率」

一致率衡量的是**逐指令对齐度**，不是「能不能用」。

- `100%` = 与原字节码逐函数完全一致，可以确信行为等同原程序
- `< 100%` = 存在写法差异。**多数是无害的**（如 `x if x else y` 与
  `x or y` 语义等价，但编译出的跳转指令不同），但需要人工确认每一处

判断是否真有问题，看差异描述里的关键词：

- 「缺少字面量 / 变量 / 名字」→ **要警惕**，可能真漏了东西
- 「分支数不同」→ 要看看是不是漏了分支
- 「(提示) 跳转写法略有差异，语义可能等价」→ 通常无害

## 当前状态

| 模块 | 一致率 |
|---|---|
| `src/pan123_api.py` | 100% |
| `src/tasks.py` | 100% |
| `src/server.py` | 73% |
| `src/library_store.py` | 66% |

四个模块均已在真实环境验证可正常启动、加载影库、搜索、导出。

---

# 二、mem_test.py —— 影库内存测试

## 它解决什么问题

点「追加影库」后进程**瞬间消失、日志无记录** —— 这是 **OOM** 的典型特征：
内存被撑爆后内核用 `SIGKILL` 杀进程，不是程序抛异常，所以什么都不打印。

本工具在**本地**（不需要 Docker）测出每个影库的加载内存，
在你把机器搞崩之前就能看出趋势。

## 用法

```bash
# 逐个影库加载（每个加载后释放）
python tools/mem_test.py

# ★ 模拟「追加」：全部保持常驻，复现内存累加
python tools/mem_test.py --append

# 设定内存上限，超了判定为「会崩」
python tools/mem_test.py --append --limit 1024

# 对比拆分方案：把拆分目录当小库加载
python tools/mem_test.py --compare ./瘦身输出
```

**判读**：看输出最后一行的「当前进程内存」。若接近或超过目标环境可用内存，
就是会崩。

## 实测参考（192.7 MB / 746,686 条）

| 指标 | 数值 |
|---|---|
| 加载后常驻 | 845 MB |
| 加载峰值 | ~1,500 MB |
| 加载耗时 | 12.6 秒 |

经验公式：**峰值 ≈ 影库体积 × 7.8**

## 真因（实测定位）

`Library.load()` 里 `json.load` 解析出的**完整原始 dict 无法释放**，
与解析后的对象同时驻留。tracemalloc 显示：

```
343 MB   json/decoder.py:361        ← 原始 dict，load() 返回后仍存活
152 MB   library_store.py:206       ← entry['type'] 字段
 47 MB   library_store.py:199       ← entry{'path','etag','size'}
```

详见根目录 `追加影库崩溃-本地复现与真因.md`。

---

# 三、split_library.py —— 影库拆分

## 它解决什么问题

把大影库拆成多个小库，**降低单次加载峰值**，避免小内存环境加载时 OOM。

⚠️ **注意**：拆分**只降峰值，不降常驻总量**（记录总数不变）。
实测 192.7 MB 拆成 24 个小库后，常驻 845 MB → 632 MB（仅降 25%）。

## 用法

```bash
# 查看规模与峰值预估（含顶级分组分布）
python tools/split_library.py "影库.json" --info

# 按分类目录拆，每库最多 5 万条（推荐）
python tools/split_library.py "影库.json" --by-dir 50000

# 按条数顺序切块
python tools/split_library.py "影库.json" --split 50000

# 只留某类
python tools/split_library.py "影库.json" --filter "电影/" --by-dir 50000

# 预览不落盘
python tools/split_library.py "影库.json" --by-dir 50000 --dry-run
```

输出目录默认 `瘦身输出/`，可用 `-o` 改。输出的 JSON 保留原影库元信息结构，
可直接放回数据目录被程序加载。
