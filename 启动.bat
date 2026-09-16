@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ================================================================
echo   123云盘影库搜索工具 - 本地启动
echo ================================================================
echo.

REM ---- 按优先级找「可用的」Python（必须能 import requests）----
set PYEXE=

for %%P in (
    "%~dp0.venv\Scripts\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
) do (
    if exist %%P (
        %%P -c "import requests" >nul 2>nul
        if not errorlevel 1 (
            set PYEXE=%%~P
            goto :found
        )
    )
)

REM 回退：PATH 里的 python / py
python -c "import requests" >nul 2>nul
if not errorlevel 1 (
    set PYEXE=python
    goto :found
)
py -3 -c "import requests" >nul 2>nul
if not errorlevel 1 (
    set PYEXE=py -3
    goto :found
)

REM 都没找到 → 给出明确指引
echo   [错误] 没找到可用的 Python 环境（需要 requests 库）
echo.
echo   你机器上可能装了 Python，但缺少 requests 依赖。
echo   请执行以下任一步骤：
echo.
echo     方式一：安装依赖（推荐）
echo         pip install requests
echo.
echo     方式二：如果没有 Python，先安装
echo         https://www.python.org/downloads/
echo         （安装时务必勾选 "Add Python to PATH"）
echo.
pause
exit /b 2

:found
echo   使用 Python: %PYEXE%
echo.

%PYEXE% "本地启动.py"
set RC=%errorlevel%

echo.
if not "%RC%"=="0" (
    echo   启动失败（退出码 %RC%），请把上面的信息截图反馈。
)
echo   服务已停止。
pause
exit /b %RC%
