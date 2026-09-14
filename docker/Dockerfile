#
# 123云盘影库搜索工具 —— 容器镜像
#
# 设计思路：不重写业务代码，而是把 Windows 版 exe（PyInstaller 产物）里的
# Python 字节码与前端静态资源在**构建阶段**抽出来，再交给容器里的官方
# CPython 3.13 直接执行。这样容器版与桌面版出自同一份构建产物，功能与
# 行为天然一致，后续换新 exe 重新 build 即可，无需维护两套代码。
#
FROM python:3.13-slim

LABEL org.opencontainers.image.title="123云盘影库搜索工具" \
      org.opencontainers.image.description="123云盘秒传影库管理工具 V1.0.3（Docker 版）" \
      org.opencontainers.image.source="https://github.com/sadmion/123-"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LB_BROWSER=1 \
    LB_DATA_ROOT=/data \
    APP_DIR=/app \
    TZ=Asia/Shanghai

WORKDIR /app

# 运行依赖：requests（123云盘接口）、segno（扫码登录二维码生成）
# 国内网络较慢时可改用镜像源（把下面一行换成被注释的那行）：
# RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple requests segno
RUN pip install --no-cache-dir requests segno

# ① 抽出 exe 内的字节码与静态资源（丢弃 Windows 专用 DLL/PYD）
COPY ["123云盘影库搜索工具.exe", "/tmp/app.exe"]
COPY docker/extract_pyinstaller.py /tmp/extract_pyinstaller.py
RUN python /tmp/extract_pyinstaller.py /tmp/app.exe --linux -o /app \
    && rm -f /tmp/app.exe /tmp/extract_pyinstaller.py \
    && echo "--- 镜像内应用文件 ---" && ls -la /app

# ② 容器启动器：改监听地址为 0.0.0.0、屏蔽桌面壳、准备数据目录
COPY docker/entry.py /app/entry.py

VOLUME ["/data"]
EXPOSE 5890

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5890/api/login/status',timeout=3).status==200 else 1)"]

CMD ["python", "/app/entry.py"]
