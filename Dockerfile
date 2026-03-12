FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY templates/ ./templates/

# 复制环境变量示例（实际使用时需要创建 .env 文件）
COPY .env.example .env

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "src/web_app.py"]
