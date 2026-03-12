#!/bin/bash

# Agent 系统安装脚本 (Linux/Mac)
# 使用方式：chmod +x install.sh && ./install.sh

set -e

echo "======================================"
echo "   Agent 系统安装脚本 (Linux/Mac)"
echo "======================================"
echo ""

# 检查 Python 版本
echo "🔍 检查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.10 或更高版本"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "MacOS: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本：$PYTHON_VERSION"

# 检查 pip
echo ""
echo "🔍 检查 pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：未找到 pip"
    echo "请安装 pip: sudo apt install python3-pip 或 curl https://bootstrap.pypa.io/get-pip.py | python3"
    exit 1
fi
echo "✅ pip 已安装"

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，是否删除重建？(y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ 虚拟环境已重建"
    else
        echo "✅ 使用现有虚拟环境"
    fi
else
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
echo ""
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo ""
echo "📦 升级 pip..."
pip install --upgrade pip -q

# 安装依赖
echo ""
echo "📦 安装依赖包..."
pip install -r requirements.txt

echo ""
echo "✅ 依赖安装完成"

# 创建 .env 文件
echo ""
echo "🔧 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填入你的 API Key"
    echo "   使用命令：nano .env 或 vim .env"
else
    echo "✅ .env 文件已存在"
fi

# 安装完成
echo ""
echo "======================================"
echo "   🎉 安装完成！"
echo "======================================"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入你的 API Key"
echo "2. 运行启动脚本：./start.sh"
echo "3. 访问：http://localhost:5000"
echo ""
echo "测试安装："
echo "  - 运行测试：pytest tests/ -v"
echo "  - 查看覆盖率：pytest --cov=src tests/"
echo ""
echo "如需卸载，删除 venv 文件夹即可：rm -rf venv"
echo ""
