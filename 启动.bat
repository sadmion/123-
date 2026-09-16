@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

echo.
echo ============================================================
echo   123 YunPan Library Search - Local Launcher
echo ============================================================
echo.

set "PYEXE="

REM ---- Look for a Python that can import requests ----
REM 1) project venv
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" -c "import requests" >nul 2>nul
    if not errorlevel 1 set "PYEXE=%~dp0.venv\Scripts\python.exe"
)

REM 2) common install locations
if not defined PYEXE (
    for %%D in (
        "%LOCALAPPDATA%\Programs\Python\Python313"
        "%LOCALAPPDATA%\Programs\Python\Python312"
        "%LOCALAPPDATA%\Programs\Python\Python311"
        "%LOCALAPPDATA%\Programs\Python\Python310"
        "C:\Python313"
        "C:\Python312"
        "C:\Python311"
    ) do (
        if not defined PYEXE (
            if exist "%%~D\python.exe" (
                "%%~D\python.exe" -c "import requests" >nul 2>nul
                if not errorlevel 1 set "PYEXE=%%~D\python.exe"
            )
        )
    )
)

REM 3) PATH
if not defined PYEXE (
    python -c "import requests" >nul 2>nul
    if not errorlevel 1 set "PYEXE=python"
)
if not defined PYEXE (
    py -3 -c "import requests" >nul 2>nul
    if not errorlevel 1 set "PYEXE=py -3"
)

if not defined PYEXE goto :nopython

echo   Using Python: %PYEXE%
echo.
"%PYEXE%" "%~dp0run.py"
set "RC=%errorlevel%"
goto :done

:nopython
echo   [ERROR] No usable Python found (needs the "requests" module).
echo.
echo   Option 1 - Install the dependency (if Python is already installed):
echo       pip install requests
echo.
echo   Option 2 - Install Python first:
echo       https://www.python.org/downloads/
echo       IMPORTANT: check "Add Python to PATH" during setup.
echo.
set "RC=2"

:done
echo.
if not "%RC%"=="0" echo   Launcher exited with code %RC%. Please report the message above.
echo   Server stopped.
pause
exit /b %RC%
