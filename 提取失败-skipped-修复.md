# 提取失败: 'skipped' —— 原因与修复

## 一句话结论

**服务端存在一个旧格式的「提取断点文件」**（缺 `skipped` 字段），
恢复提取时程序用硬下标读取该字段，抛出 `KeyError: 'skipped'`。

**修复：** 跑 `python 断点修复.py --fix` 补齐字段；或 `--clear` 删掉断点重新提取。

---

## 一、原因（已从字节码确认）

程序支持分享提取的**断点续传**，断点文件位于：

```
<数据目录>/_checkpoints/extract_<分享key>.json
```

**写入**断点（`tasks.ExtractTask._save_checkpoint`）时包含 7 个字段：

```python
ck = {
    'shareKey':    ...,
    'total_files': ...,
    'scanned':     ...,
    'skipped':     ...,     # ← 写的时候有
    'done_dirs':   ...,
    'file_filters':...,
    'ts':          ...,
}
```

**读取**断点（`pan123_api.share_walk`）时：

```python
scanned   = resume_offset['scanned']                      # 硬下标
skipped   = resume_offset['skipped']                      # 硬下标 ← KeyError
done_dirs = set(resume_offset.get('done_dirs') or [])     # 这个却用了 .get()
```

**注意这个不对称**：`done_dirs` 做了兼容处理（`.get()`），
但 `scanned` / `skipped` 用的是**硬下标** `[...]`。

所以当断点文件是**旧版本程序写的**（没有 `skipped` 字段）时，
恢复提取会立刻抛 `KeyError: 'skipped'`，前端显示：

```
提取失败: 'skipped'
```

**这不是新出现的 bug，而是旧断点数据与新版代码的格式不兼容。**

---

## 二、修复

### 方法 1：补齐字段（保留提取进度，推荐）

```bash
# 先看看有哪些断点、缺什么
python 断点修复.py --list

# 补齐缺失字段（原文件会备份为 .bak）
python 断点修复.py --fix
```

输出示例：

```
断点目录: .../data/_checkpoints
断点文件: 1 个

  extract_sESGsjv-Tzfpd.json
    shareKey   : 'sESGsjv-Tzfpd'
    total_files: 1200   scanned: 300   skipped: None
    done_dirs  : 2 个
    ⚠ 缺失字段: skipped, file_filters   ← 会导致 KeyError
```

修复后：

```
extract_sESGsjv-Tzfpd.json 已补齐: skipped, file_filters
修复完成：1 个文件
原文件已备份为 *.bak，可重新发起提取。
```

**原有的扫描进度会被保留**，可以继续断点续传。

### 方法 2：删除断点（重新开始提取）

```bash
python 断点修复.py --clear --yes
```

提取会从头开始，适合不在意已扫描进度的场景。

### 方法 3：在网页上操作

程序本身有断点管理接口：

```
GET  /api/extract/checkpoint          # 查看断点列表
POST /api/extract/checkpoint/delete   # 删除断点
```

在「秒传提取·分享入库」面板里通常有对应的删除/清空入口。

### 如果数据目录不在默认位置

```bash
python 断点修复.py --list --data-root "D:/123data"
```

---

## 三、为什么会出现旧格式断点

| 场景 | 说明 |
|---|---|
| **升级过程序版本** | V1.0.3 之前的版本写的断点缺 `skipped` 字段 |
| **提取中途被中断** | 断电、杀进程、任务被停止，留下不完整的断点 |
| **手动改过断点文件** | 手工编辑导致字段缺失 |

---

## 四、预防建议

1. **升级程序后**，先清一次旧断点：`python 断点修复.py --clear --yes`
2. **提取大分享时不要中途强杀进程**，用界面上的「停止」按钮（会正常保存断点）
3. 遇到 `KeyError: 'xxx'` 形式的报错，基本都是**数据格式与代码版本不匹配**，
   优先考虑清理对应的数据文件

---

## 五、这是程序本身的缺陷吗

**算是一个健壮性缺陷。** 同一个函数里，`done_dirs` 用 `.get()` 做了防御，
但 `scanned` / `skipped` 用硬下标——**风格不一致**，导致旧数据直接崩溃。

要彻底修好需要改源码，把那两行改成：

```python
scanned = resume_offset.get('scanned', 0)
skipped = resume_offset.get('skipped', 0)
```

但当前项目只有 exe（源码为约 81% 覆盖率的反编译还原稿），
**改不了内部代码**，所以采用「外部工具修复数据」的方案。

> 若将来拿到完整源码，这是**一行就能修好**的问题，值得一并处理。

---

*诊断时间：2026-09-15 ｜ 依据：字节码反编译分析 + 模拟读取验证*
