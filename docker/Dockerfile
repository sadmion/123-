#
# 123云盘影库搜索工具 —— 容器镜像（源码版）
#
# 设计思路：直接构建 src/ 下的源码，不再从桌面版 exe 抽字节码。
# 这样改代码 → 推仓库 → CI 重建镜像即可，无需重新打包 exe。
#
FROM python:3.13-slim

LABEL org.opencontainers.image.title="123云盘影库搜索工具" \
      org.opencontainers.image.description="123云盘秒传影库管理工具 V1.0.3（Docker 源码版）" \
      org.opencontainers.image.source="https://github.com/sadmion/123-"

# 版本号：由 CI 从 git tag 传入（--build-arg APP_VERSION=1.0.5）。
# 未传时为 "dev"，页面显示 dev 便于区分"非发布构建"。
ARG APP_VERSION="dev"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LB_BROWSER=1 \
    LB_DATA_ROOT=/data \
    APP_DIR=/app \
    TZ=Asia/Shanghai \
    LB_VERSION="V${APP_VERSION}"

WORKDIR /app

# 运行依赖：requests（123云盘接口）、segno（扫码登录二维码生成）
# 国内网络较慢时可改用镜像源（把下面一行换成被注释的那行）：
# RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple requests segno
RUN pip install --no-cache-dir requests segno

# ① 源码 + 前端静态资源（同目录，server.py 按 __file__ 定位）
COPY src/ /app/src/

# ② 容器启动器：改监听地址为 0.0.0.0、屏蔽桌面壳、准备数据目录
COPY docker/entry.py /app/entry.py

# 构建期自检：确保 4 个模块与前端资源都在，且源码可编译
RUN python - <<'PY'
import compileall, os, sys
need = ['server.py', 'pan123_api.py', 'tasks.py', 'library_store.py',
        'index.html', 'style.css', 'app.js', 'bgm.mp3']
miss = [n for n in need if not os.path.exists('/app/src/' + n)]
if miss:
    sys.exit('缺少文件: %s' % ', '.join(miss))
if not compileall.compile_dir('/app/src', quiet=1):
    sys.exit('源码编译失败')
print('--- 镜像内应用文件 ---')
for n in sorted(need):
    print('  %-18s %8d B' % (n, os.path.getsize('/app/src/' + n)))
PY

VOLUME ["/data"]
EXPOSE 5890

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5890/api/login/status',timeout=3).status==200 else 1)"]

CMD ["python", "/app/entry.py"]
