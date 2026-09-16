# 123云盘影库搜索工具

管理 123 云盘「秒传链接」影库的工具：按片名搜索作品、按分类浏览、导出秒传文件、从分享链接提取新影库，并把秒传文件批量导入自己的 123 云盘。

**V1.0.5** · 源码 + Docker 部署

## 部署

镜像已发布到 GitHub 容器仓库（GHCR），支持 `linux/amd64` 与 `linux/arm64`。

### 方式一：拉取现成镜像（推荐）

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

### 方式二：Compose 编排

仓库备有两份可直接使用的 compose 文件：

| 文件 | 用途 |
|---|---|
| [`compose-镜像版.yml`](compose-镜像版.yml) | 纯拉取 GHCR 镜像，只需一个文件 + `data` 目录 |
| [`compose-本地构建.yml`](compose-本地构建.yml) | 从本仓库 `src/` 现场构建，不依赖 GHCR |
| [`docker-compose.yml`](docker-compose.yml) | 主配置，变量驱动（可构建可拉取，支持换端口/换 tag） |

```bash
# 镜像版
curl -O https://raw.githubusercontent.com/sadmion/123-/main/compose-镜像版.yml
mv compose-镜像版.yml docker-compose.yml
mkdir -p data && docker compose up -d

# 本地构建版
git clone https://github.com/sadmion/123-.git && cd 123-
mkdir -p data && docker compose up -d --build
```

完整部署、运维命令、数据备份、故障排查见 **[`docker/维护手册.md`](docker/维护手册.md)**。

> 首次拉取若报 `unauthorized`：GHCR 镜像默认私有，到仓库的 `Packages` → `Package settings` 里改成 `Public` 即可。

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
docker/
  Dockerfile        镜像构建（直接构建 src/ 源码）
  entry.py          容器启动器（监听 0.0.0.0、跳过桌面壳、预建数据目录）
  selfcheck.py      构建自检（30 项，含真实启动探活，不需要 Docker）
  维护手册.md       Docker 部署运维主手册
tools/
  verify_src.py     源码还原校验器（比对源码与原始字节码）
```

## 发布新版本

改完 `src/` 下的代码后：

```bash
python 发布新版本.py --version 1.0.6 --note "改了什么"
```

这条命令会依次完成：**自检 → 提交 → 打 tag → 推送**，GitHub Actions 随后自动构建镜像并推送到 GHCR。

构建完成后，服务器上更新：

```bash
docker compose pull && docker compose up -d
```

> 版本号由构建时从 git tag 注入（`LB_VERSION` 环境变量），页面显示的版本与镜像 tag 自动保持一致。

## 功能速览

- **搜索**：片名 / 目录名 / 分类名模糊匹配，关键词 ≥2 字
- **分类浏览**：标签筛选、折叠，多选后合并导出
- **作品卡片**：片名、年份、视频数、体积，可展开勾选部分导出，海报取自 TMDB
- **导出**：生成标准 `.123fastlink.json` 秒传文件
- **分享提取**：支持带提取码、批量多行，可断点续扫
- **秒传导入**：Bearer Token / 扫码 / 账号密码三种登录，走官方秒传接口不消耗流量
- **背景音乐**：内置曲目，可自定义 `bgm.mp3`

详细使用说明见 [`使用说明.md`](使用说明.md)，版本变更见 [`版本更新说明.md`](版本更新说明.md)。

## 安全提醒

本工具没有账号体系，**能访问端口就能使用其中的 123 云盘登录态**。请只在局域网 / 家庭 NAS 使用，不要直接暴露到公网；外网访问请加反向代理认证或走 VPN。

登录凭据保存在数据目录的 `记录数据存放目录【勿动】/.login.json`，已在 `.gitignore` 中排除，请勿提交到公开仓库。
