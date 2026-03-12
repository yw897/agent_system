@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ======================================
echo    Agent 系统安装脚本 (Windows)
echo ======================================
echo.

REM 检查 Python 版本
echo 🔍 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    echo.
    echo 请先安装 Python 3.10 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python 版本：!PYTHON_VERSION!

REM 检查 pip
echo.
echo 🔍 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 pip
    echo 请重新安装 Python 并确保勾选 "Add Python to PATH"
    pause
    exit /b 1
)
echo ✅ pip 已安装

REM 创建虚拟环境
echo.
echo 📦 创建虚拟环境...
if exist "venv" (
    echo ⚠️  虚拟环境已存在
    set /p REBUILD="是否删除重建？(y/N): "
    if /i "!REBUILD!"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo ✅ 虚拟环境已重建
    ) else (
        echo ✅ 使用现有虚拟环境
    )
) else (
    python -m venv venv
    echo ✅ 虚拟环境已创建
)

REM 激活虚拟环境
echo.
echo 📦 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级 pip
echo.
echo 📦 升级 pip...
python -m pip install --upgrade pip -q

REM 安装依赖
echo.
echo 📦 安装依赖包...
pip install -r requirements.txt

echo.
echo ✅ 依赖安装完成

REM 创建 .env 文件
echo.
echo 🔧 配置环境变量...
if not exist ".env" (
    copy .env.example .env >nul
    echo ✅ 已创建 .env 文件
    echo.
    echo ⚠️  请编辑 .env 文件，填入你的 API Key
    echo    使用记事本打开：notepad .env
) else (
    echo ✅ .env 文件已存在
)

REM 安装完成
echo.
echo ======================================
echo    🎉 安装完成！
echo ======================================
echo.
echo 下一步：
echo 1. 编辑 .env 文件，填入你的 API Key
echo 2. 运行启动脚本：start.bat
echo 3. 访问：http://localhost:5000
echo.
echo 测试安装：
echo   - 运行测试：pytest tests -v
echo   - 查看覆盖率：pytest --cov=src tests
echo.
echo 如需卸载，删除 venv 文件夹即可
echo.
pause
