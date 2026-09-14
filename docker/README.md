# Docker Compose 部署说明

容器版与 Windows 版**功能完全一致**：同一份构建产物，只是换了运行方式。适合跑在 NAS、Linux 服务器、软路由上，用浏览器从局域网任意设备访问。

---

## 一、快速开始

### 方式一：直接拉镜像（推荐，无需构建）

镜像已发布在 GitHub 容器仓库，任何 x86_64 / ARM 服务器都能直接拉取，**不需要本机有构建环境、也不需要 Windows 机器**：

```bash
# 1. 进入项目目录（含 docker-compose.yml 的那层）
cd 123搜索工具

# 2. 拉取并启动（默认使用 ghcr.io/sadmion/123-:latest）
docker compose up -d

# 3. 浏览器访问
http://<部署机器的IP>:5890/
```

前提：项目目录里要有 `docker-compose.yml`。若只想拷这一个文件到别处，记得同时保证 `./data` 目录可用（会自动创建）。

### 方式二：从源码本地构建

改了代码或想自己编译时：

```bash
docker compose up -d --build
```

首次构建约 1~3 分钟（装依赖 + 从 exe 抽包）。构建用的 exe 就在仓库里，克隆后即可直接 build。

### 验证是否启动成功

```bash
docker compose ps          # 期望 STATUS 为 Up (healthy)
docker compose logs -f     # 看到下面这行即正常
```

```
123云盘影库搜索工具 V1.0.3  数据目录: /data  http://127.0.0.1:5890/
```

## 二、镜像说明

| 项目 | 内容 |
|---|---|
| 镜像地址 | `ghcr.io/sadmion/123-:latest`（另含 `:v1.0.3` 等版本标签） |
| 支持架构 | `linux/amd64`、`linux/arm64`（NAS、树莓派、ARM 云主机均可） |
| 构建方式 | 打 `v*` 标签时由 GitHub Actions 自动构建推送（见 `.github/workflows/docker-publish.yml`） |
| 手动更新 | `docker compose pull && docker compose up -d` |

> **GHCR 镜像默认是私有的**，首次在其他服务器拉取会报 `unauthorized`。两种处理方式：
> - **公开**（推荐，最省事）：GitHub 仓库页 → 右侧 `Packages` → 点开该镜像 → `Package settings` → 底部 `Change visibility` → 改为 `Public`。
> - **保持私有**：登录后再拉
>   ```bash
>   echo <你的GitHub个人访问令牌> | docker login ghcr.io -u sadmion --password-stdin
>   ```
>   令牌需勾选 `read:packages` 权限（Settings → Developer settings → Personal access tokens）。

### 极简部署：只拷一个文件到目标服务器

不想克隆整个仓库（仓库里有 60MB 的 exe 影库清单），可直接在目标服务器建一个目录，放下面这个 `docker-compose.yml` 即可：

```yaml
services:
  pan123-library:
    image: ghcr.io/sadmion/123-:latest
    container_name: pan123-library
    restart: unless-stopped
    ports:
      - "5890:5890"
    environment:
      TZ: Asia/Shanghai
      LB_BROWSER: "1"
      LB_DATA_ROOT: /data
    volumes:
      - ./data:/data
```

然后 `docker compose up -d`，再把影库 JSON 放进 `./data/秒传文件导入或追加/`。

## 三、目录与数据

```
123搜索工具/
├── docker-compose.yml          # 编排文件（根目录）
├── .github/workflows/          # 自动构建镜像的 CI 配置
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

**换机器 / 备份**：整个 `data/` 拷走即可，登录态、影库、断点记录都在里面。

**权限问题**：容器以 root 运行，生成的 `data/` 文件属主是 root。若在 NAS 上遇到无法编辑，执行一次 `sudo chown -R $(id -u):$(id -g) data` 即可。

## 四、常用操作

```bash
docker compose logs -f                # 看实时日志
docker compose restart                # 重启
docker compose down                   # 停止并删除容器（data/ 不受影响）
docker compose pull && docker compose up -d   # 更新到最新镜像
docker compose up -d --build          # 用本地代码重新构建
LB_PORT=8080 docker compose up -d     # 换宿主机端口为 8080
docker compose exec pan123-library ls /data    # 进容器查看数据目录
```

## 五、工作原理（为什么 Windows 的 exe 能在 Linux 容器里跑）

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

业务代码**一行未改**——后续用 PyInstaller 重新打包 exe 后，重新构建镜像即可同步更新。

## 六、常见问题

| 现象 | 原因与处理 |
|---|---|
| `docker: command not found` | 先装 Docker；NAS 一般在套件中心装 Docker / Container Manager |
| 拉镜像报 `unauthorized` / `denied` | GHCR 镜像默认私有，按第二节改成 Public，或先 `docker login ghcr.io` |
| 启动后访问不了 | ①端口被占用 `netstat -tlnp \| grep 5890`；②云服务器需在安全组放行；③改了 `LB_PORT` 后要用新端口访问 |
| 日志报 `未选择数据目录, 退出` | 数据目录不存在：确认 `./data` 可创建，或 `LB_DATA_ROOT` 指向的路径已存在 |
| 容器不断重启 | 看 `docker compose logs` 报错；多为端口冲突或 data 目录无写权限 |
| 扫码登录二维码不显示 | 镜像已装 `segno`；若自行裁剪依赖导致，补装后再启动 |
| 构建反复失败 | `docker/Dockerfile` 里已备好 pip 国内源（注释形式）；基础镜像拉取慢可给 Docker 配镜像加速 |
| `data/` 里文件改不动 | 见第三节权限说明，`chown` 一次即可 |
| 旧版 ARM 设备不支持 | 镜像已出 arm64；若设备过老（armv7 32 位）需自行在设备上 `--build` |

## 七、安全提示

- 工具本身没有账号体系，**谁访问得到这个端口，谁就能用你的 123 云盘登录态**。仅限内网 / 家庭 NAS 使用，不要直接映射到公网。
- 确实需要外网访问，请套一层反向代理加认证（如 Nginx + Basic Auth），或只走 VPN / 内网穿透的白名单。
- `data/记录数据存放目录【勿动】/.login.json` 保存的是 123 云盘登录凭据，**不要提交到任何公开仓库**（已在本项目 `.gitignore` 中排除）。
- 容器以 root 运行。若你更在意隔离，可在 compose 里加 `user: "1000:1000"` 并确保 `./data` 属主对应（注意需自行处理目录权限）。
