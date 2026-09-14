# Docker Compose 部署说明

容器版与 Windows 版**功能完全一致**：同一份构建产物，只是换了运行方式。适合跑在 NAS、Linux 服务器、软路由上，用浏览器从局域网任意设备访问。

---

## 一、快速开始

```bash
# 1. 进入项目目录（含 docker-compose.yml 的那层）
cd 123搜索工具

# 2. 构建并启动
docker compose up -d --build

# 3. 浏览器访问
http://<部署机器的IP>:5890/
```

首次启动约 1~2 分钟（装依赖 + 抽包）。用 `docker compose logs -f` 看到下面这行就算起来了：

```
123云盘影库搜索工具 V1.0.3  数据目录: /data  http://127.0.0.1:5890/
```

## 二、目录与数据

```
123搜索工具/
├── docker-compose.yml          # 编排文件（根目录）
├── docker/
│   ├── Dockerfile              # 镜像构建
│   ├── entry.py                # 容器启动器（容器适配层）
│   └── extract_pyinstaller.py  # 构建时从 exe 抽字节码
└── data/                       # ← 所有运行数据都在这（自动创建，已被 .gitignore 排除）
    ├── 秒传文件导入或追加/      # 你的影库 JSON 放这里
    ├── 秒传文件导出/            # 导出的秒传文件
    ├── 记录数据存放目录【勿动】/  # 登录凭据、历史、配置
    └── logs/server.log          # 运行日志
```

**导入自己的影库**：把 `xxx.123fastlink.json` 丢进 `./data/秒传文件导入或追加/`，程序会自动监听并加载，无需重启。

**换机器/备份**：整个 `data/` 拷走即可，登录态、影库、断点记录都在里面。

## 三、常用操作

```bash
docker compose logs -f          # 看实时日志
docker compose restart          # 重启
docker compose down             # 停止并删除容器（data/ 不受影响）
docker compose up -d --build    # 更新了 exe 或代码后重新构建
LB_PORT=8080 docker compose up -d   # 换宿主机端口为 8080
```

## 四、工作原理（为什么 Windows 的 exe 能在 Linux 容器里跑）

exe 是 PyInstaller 单文件产物，里面装的是 **CPython 3.13 字节码**，本身与操作系统无关——真正不能跨平台的是它的 Windows 引导器和一堆 `.dll/.pyd`。于是镜像构建时：

1. `extract_pyinstaller.py` 解析 exe 里的 PyInstaller 归档（含 overlay 偏移换算），取出：
   - 入口脚本 `server.pyc`
   - 自有模块 `pan123_api.pyc`、`tasks.pyc`、`library_store.pyc`（取自 PYZ）
   - 前端资源 `index.html` / `style.css` / `app.js` / `bgm.mp3`
   - 丢弃所有 `.dll/.pyd` 等 Windows 专用二进制
2. 用镜像内 Python 的 magic 重写 pyc 头（exe 由 3.13 早期小版本编译，magic 与新版不同，照搬会 `bad magic number`）
3. `entry.py` 以 `__main__` 方式加载并执行 `server.pyc`，同时做三项容器适配：
   - 程序内部硬编码监听 `127.0.0.1` → 改写为 `0.0.0.0`
   - 屏蔽 pywebview 桌面窗口与 `webbrowser` 拉起（容器无 GUI），改为打印访问地址
   - 提前创建数据目录（程序要求目录必须已存在，否则会转去弹 tkinter 选择框并退出）

业务代码**一行未改**——后续用 PyInstaller 重新打包 exe 后，`docker compose up -d --build` 即可同步更新容器版。

## 五、常见问题

| 现象 | 原因与处理 |
|---|---|
| `docker: command not found` | 先装 Docker（NAS 一般在套件中心装 Docker/Container Manager） |
| 启动后访问不了 | ①确认端口映射未被占用 `netstat -tlnp \| grep 5890`；②云服务器需在安全组放行端口；③`LB_PORT` 改端口后记得用新端口访问 |
| 日志报 `未选择数据目录, 退出` | 数据目录不存在：确认 `./data` 可创建，或 `LB_DATA_ROOT` 指向的路径已存在 |
| 容器不断重启 | 看 `docker compose logs` 报错；多为端口冲突或 data 目录无写权限 |
| 扫码登录二维码不显示 | 镜像已装 `segno`；若自行裁剪依赖导致，补装后再启动 |
| 构建很慢/超时 | 已通过 `.dockerignore` 排除 200MB+ 的影库清单；pip 慢可换国内源（`docker/Dockerfile` 里有注释好的清华源），基础镜像拉取慢可给 Docker 配置镜像加速 |
| ARM 设备（树莓派等） | 无需特殊处理：镜像是纯 Python 字节码，构建时在目标架构上直接跑即可（不要用 x86 机器构建后拷 arm 镜像） |

## 六、安全提示

- 工具本身没有账号体系，**谁访问得到这个端口，谁就能用你的 123 云盘登录态**。仅限内网/家庭 NAS 使用，不要直接映射到公网。
- 确实需要外网访问，请套一层反向代理加认证（如 Nginx + Basic Auth），或只走 VPN/内网穿透的白名单。
- `data/记录数据存放目录【勿动】/.login.json` 保存的是 123 云盘登录凭据，**不要提交到任何公开仓库**（已在本项目 `.gitignore` 中排除）。
