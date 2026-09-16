# 123云盘影库搜索工具

管理 123 云盘「秒传链接」影库的工具：按片名搜索作品、按分类浏览、导出秒传文件、从分享链接提取新影库，并把秒传文件批量导入自己的 123 云盘。

**V1.0.6** · 源码 + Docker 部署

## 部署

镜像已发布到 GitHub 容器仓库（GHCR），支持 `linux/amd64` 与 `linux/arm64`。

### 方式一：compose 编排（推荐）

仓库根目录有 `docker-compose.yml`，支持两种用法：

```bash
# 拉取 GHCR 现成镜像
mkdir -p data && docker compose up -d

# 或从本仓库 src/ 现场构建（不依赖 GHCR）
git clone https://github.com/sadmion/123-.git && cd 123-
mkdir -p data && docker compose up -d --build
```

换端口 / 换镜像版本用环境变量：

```bash
LB_PORT=8080 docker compose up -d
LB_TAG=1.0.6 docker compose up -d
LB_IMAGE=ghcr.io/sadmion/pan123-library docker compose pull && docker compose up -d
```

### 方式二：docker run

```bash
docker run -d --name pan123-library \
  -p 5890:5890 \
  -v "$PWD/data:/data" \
  -e TZ=Asia/Shanghai \
  -e LB_BROWSER=1 \
  --restart unless-stopped \
  ghcr.io/sadmion/pan123-library:latest
```

然后浏览器访问 `http://<机器IP>:5890/`。

**完整部署、运维命令、数据备份、故障排查、版本发布见
[`docker/维护手册.md`](docker/维护手册.md)。**

> 首次拉取若报 `unauthorized`：GHCR 镜像默认私有，到仓库的 `Packages` →
  `Package settings` 里改成 `Public` 即可。

## 本地运行（不用 Docker）

```bash
# 首次准备
python -m venv .venv
.venv/Scripts/python.exe -m pip install requests    # Windows
# .venv/bin/python -m pip install requests          # macOS / Linux

# 启动（Windows 也可直接双击 启动.bat）
python run.py
```

详见 [`使用说明.md`](使用说明.md)。

## 源码结构

```
src/
  pan123_api.py     API 封装：登录、分享解析、目录操作、秒传上传
  tasks.py          后台任务：分享提取（断点续传）、秒传导入
  library_store.py  影库数据层：加载、分类聚合、搜索、导出
  server.py         HTTP 服务 + API 路由 + 程序入口
  index.html        前端页面
  style.css         样式
  app.js            前端逻辑
  bgm.mp3           内置背景音乐
docker/
  Dockerfile        镜像构建（直接构建 src/ 源码）
  entry.py          容器启动器（监听 0.0.0.0、跳过桌面壳、预建数据目录）
  selfcheck.py      构建自检（31 项，含真实启动探活，不需要 Docker）
  维护手册.md        部署运维 + 版本发布主手册
tools/
  verify_src.py     源码还原校验器（比对源码与原始字节码）
  mem_test.py       影库内存测试（诊断「追加影库崩溃」）
  split_library.py  影库拆分（降低加载峰值）
run.py              本地启动器（python run.py 或双击）
启动.bat            Windows 双击启动
发布新版本.py        一键发布（自检 → 提交 → 打 tag → 推送）
CHANGELOG.md        版本记录
```

## 发布新版本

改完 `src/` 下的代码后：

```bash
python 发布新版本.py --version 1.0.7 --note "改了什么"
```

这条命令会依次完成：**自检 → 提交 → 打 tag → 推送**，GitHub Actions 随后自动构建镜像并推送到 GHCR。

构建完成后，服务器上更新：

```bash
docker compose pull && docker compose up -d
```

> 版本号由构建时从 git tag 注入（`LB_VERSION` 环境变量），页面显示的版本与镜像 tag 自动保持一致。

## 功能速览

- **搜索**：片名 / 目录名 / 分类名模糊匹配，关键词 ≥2 字
- **分类浏览**：标签筛选、可折叠可滚动，多选后合并导出
- **作品卡片**：片名、年份、视频数、体积，可展开勾选部分导出，海报取自 TMDB
- **导出**：生成标准 `.123fastlink.json` 秒传文件
- **分享提取**：支持带提取码、批量多行，可断点续扫
- **秒传导入**：Bearer Token / 扫码 / 账号密码三种登录，走官方秒传接口不消耗流量
- **背景音乐**：内置曲目，可自定义 `bgm.mp3`
- **右侧面板可拖动**：拖动右面板左边缘的分隔条可调宽度，双击复位

详细使用说明见 [`使用说明.md`](使用说明.md)，版本变更见 [`CHANGELOG.md`](CHANGELOG.md)。

## 安全提醒

本工具没有账号体系，**能访问端口就能使用其中的 123 云盘登录态**。请只在局域网 / 家庭 NAS 使用，不要直接暴露到公网；外网访问请加反向代理认证或走 VPN。

登录凭据保存在数据目录的 `记录数据存放目录【勿动】/.login.json`，已在 `.gitignore` 中排除，请勿提交到公开仓库。
