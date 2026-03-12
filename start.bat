@echo off
echo 🚀 启动 Agent 系统...
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo ❌ 未找到虚拟环境
    echo 请先运行：python -m venv venv
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 📦 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查依赖
echo 📦 检查依赖...
pip install -q -r requirements.txt

REM 检查 .env 文件
if not exist ".env" (
    echo ⚠️  未找到 .env 文件
    echo 正在从 .env.example 创建...
    copy .env.example .env
    echo.
    echo ❗ 请编辑 .env 文件，填入你的 API Key
    echo 然后重新运行此脚本
    pause
    exit /b 1
)

echo.
echo 🌐 启动 Web 服务...
echo 访问地址：http://localhost:5000
echo 按 Ctrl+C 停止服务
echo.

python src\web_app.py
