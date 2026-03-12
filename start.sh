#!/bin/bash

echo "🚀 启动 Agent 系统..."
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 未找到虚拟环境"
    echo "请先运行：python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "📦 检查依赖..."
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件"
    echo "正在从 .env.example 创建..."
    cp .env.example .env
    echo ""
    echo "❗ 请编辑 .env 文件，填入你的 API Key"
    echo "然后重新运行此脚本"
    exit 1
fi

echo ""
echo "🌐 启动 Web 服务..."
echo "访问地址：http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

python src/web_app.py
