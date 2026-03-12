# Agent 系统安装指南

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10+：

```bash
python --version
```

### 2. 克隆项目

```bash
cd /root/.openclaw/workspace/projects
# 项目已创建完成
```

### 3. 安装依赖

```bash
cd agent-system
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# Mac/Linux 激活虚拟环境
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 4. 配置 API Key

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 使用你喜欢的编辑器打开 .env 文件
```

在 `.env` 文件中配置：

```env
API_KEY=你的_API_Key
API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

### 5. 运行测试

```bash
# 测试工具模块
python src/tools.py

# 测试 Agent
python src/agent.py

# 运行完整测试套件
python tests/test_agent.py
python tests/test_tools.py
```

### 6. 启动 Web 服务

```bash
python src/web_app.py
```

访问：http://localhost:5000

## 功能说明

### 基础功能

- ✅ 自然语言对话
- ✅ 多轮对话历史
- ✅ 记忆系统

### 工具调用

- ✅ 计算器
- ✅ 时间/日期查询
- ✅ 文件读写
- ✅ 目录列表
- ✅ 创建提醒
- ✅ 网络搜索
- ✅ 天气查询
- ✅ 新闻获取

### 增强功能

- ✨ **打字动画** - 消息逐字显示
- ✨ **移动端适配** - 响应式布局
- ✨ **语音输入** - 语音转文字
- ✨ **用户偏好学习** - 个性化响应
- ✨ **工具调用优化** - 智能推荐
- ✨ **A/B 测试提示词** - 效果优化

## 使用示例

### 对话示例

```
👤 你：你好
🤖 AI：你好！我是你的智能助手...

👤 你：计算 123 * 456
🤖 AI：计算结果是 56088

👤 你：北京天气
🤖 AI：🌤️ 北京 天气：晴朗 25°C...

👤 你：搜索 Python 教程
🤖 AI：🔍 搜索结果...
```

### 命令行使用

```bash
# 基础对话
python src/agent.py

# 支持工具调用
python src/agent_with_tools.py

# 完整版（含学习功能）
python src/complete_agent.py
```

### Web 界面

- 标准版：http://localhost:5000
- 移动版：http://localhost:5000/mobile
- 语音版：http://localhost:5000 (默认)

## 常见问题

### Q: API Key 无效？

检查 `.env` 文件配置是否正确，确保 API Key 无空格、无换行。

### Q: 语音输入不工作？

使用 Chrome 或 Edge 浏览器，允许麦克风权限。

### Q: 移动端显示异常？

清除浏览器缓存，确保使用现代浏览器。

## 下一步

1. 根据需求添加工具
2. 优化提示词
3. 部署到服务器
4. 分享给朋友使用

祝你使用愉快！🎉
