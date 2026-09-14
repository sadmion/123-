# 123云盘影库搜索工具

管理 123 云盘「秒传链接」影库的工具：按片名搜索作品、按分类浏览、导出秒传文件、从分享链接提取新影库，并把秒传文件批量导入自己的 123 云盘。

**V1.0.3**

## 三种使用方式

| 方式 | 适合场景 | 入口 |
|---|---|---|
| 桌面版 exe | Windows 本机，双击即用（原生窗口） | `123云盘影库搜索工具.exe` |
| 浏览器版 exe | Windows 本机，无 WebView2 依赖 | `123云盘影库搜索工具浏览器版.exe` |
| **Docker / NAS 部署** | 服务器、NAS 长期挂在后台，局域网任意设备访问 | [`docker/README.md`](docker/README.md) |

三种方式功能完全一致——容器版与 exe 出自同一份构建产物。

详细功能说明见 [`使用说明.md`](使用说明.md)。

## Docker 部署（一行起）

镜像已发布到 GitHub 容器仓库，支持 `linux/amd64` 与 `linux/arm64`：

```bash
docker run -d --name pan123-library \
  -p 5890:5890 \
  -v "$PWD/data:/data" \
  -e TZ=Asia/Shanghai \
  -e LB_BROWSER=1 \
  --restart unless-stopped \
  ghcr.io/sadmion/123-:latest
```

然后浏览器访问 `http://<机器IP>:5890/`。用 Compose 编排（含端口、数据卷、健康检查）见 [`docker-compose.yml`](docker-compose.yml)，完整部署文档、常见问题与安全提示见 [`docker/README.md`](docker/README.md)。

> 首次拉取若报 `unauthorized`：GHCR 镜像默认私有，到仓库的 `Packages` → `Package settings` 里改成 `Public` 即可。

## 功能速览

- **搜索**：片名 / 目录名 / 分类名模糊匹配，关键词 ≥2 字
- **分类浏览**：标签筛选、折叠，多选后合并导出
- **作品卡片**：片名、年份、视频数、体积，可展开勾选部分导出，海报取自 TMDB
- **导出**：生成标准 `.123fastlink.json` 秒传文件
- **分享提取**：支持带提取码、批量多行，可断点续扫
- **秒传导入**：Bearer Token / 扫码 / 账号密码三种登录，走官方秒传接口不消耗流量
- **背景音乐**：内置曲目，可自定义 `bgm.mp3`

## V1.0.3 更新

- 秒传导入兼容 base62 / hex / base64 三种 etag 格式，接口域名更新
- 扫码登录改为全程复用会话，确认后可正常换取凭据
- 登录持久化，重启免登录
- 新增「停止导入」按钮
- BGM 更换并支持自定义
- 错误日志写入数据目录 `logs/server.log`

## 安全提醒

本工具没有账号体系，**能访问端口就能使用其中的 123 云盘登录态**。请只在局域网 / 家庭 NAS 使用，不要直接暴露到公网；外网访问请加反向代理认证或走 VPN。登录凭据保存在数据目录的 `记录数据存放目录【勿动】/.login.json`，已在 `.gitignore` 中排除，请勿提交到公开仓库。
