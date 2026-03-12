# Agent 系统

个人智能助手系统，支持自然语言对话、工具调用、记忆功能、语音输入和移动端适配。

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)](https://github.com/USERNAME/agent-system)

## ✨ 核心功能

- 🤖 自然语言对话
- 🔧 工具调用（计算器、搜索、天气等）
- 💾 记忆功能 + 用户偏好学习
- 🌐 Web 界面（移动端适配）
- 🎤 语音输入支持
- ✨ 打字动画效果
- ⚡ 工具调用优化
- 🧪 A/B 测试提示词

## 🚀 快速开始

### 方式一：自动安装（推荐）

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```bash
install.bat
```

安装脚本会自动：
- ✅ 检查 Python 版本（需要 3.10+）
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 创建 .env 配置文件

---

### 方式二：手动安装

**1. 创建虚拟环境**

```bash
cd agent-system
python -m venv venv
```

**2. 激活虚拟环境**

- **Windows (CMD):**
  ```bash
  venv\Scripts\activate
  ```

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```
  > ⚠️ 如果提示权限错误，运行：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

**3. 安装依赖**

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 API Key
```

在 `.env` 文件中配置：

```env
API_KEY=你的_API_Key
API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

### 3. 运行

#### 命令行版本

- **Linux/Mac:**
  ```bash
  # 基础对话
  python src/agent.py

  # 支持工具调用
  python src/agent_with_tools.py

  # 完整版（含所有功能）
  python src/complete_agent.py
  ```

- **Windows:**
  ```bash
  # 基础对话
  python src\agent.py

  # 支持工具调用
  python src\agent_with_tools.py

  # 完整版（含所有功能）
  python src\complete_agent.py
  ```

#### Web 版本

- **Linux/Mac:**
  ```bash
  python src/web_app.py
  # 或使用启动脚本
  ./start.sh
  ```

- **Windows:**
  ```bash
  python src\web_app.py
  # 或使用启动脚本
  start.bat
  ```

访问：http://localhost:5000

### 4. Docker 部署

```bash
docker-compose up -d
```

---

## 💻 Windows 用户专项说明

### 常见问题解决

**1. 虚拟环境激活失败**

如果使用 `venv\Scripts\activate` 失败，可能是 PowerShell 执行策略限制：

```powershell
# 方法 1：临时允许当前会话
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 方法 2：永久允许当前用户
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 方法 3：使用 CMD 而不是 PowerShell
cmd
venv\Scripts\activate.bat
```

**2. 路径分隔符**

Windows 使用反斜杠 `\`，但大多数命令也支持正斜杠 `/`：
- ✅ `python src\web_app.py`
- ✅ `python src/web_app.py` (也适用)

**3. 端口占用**

如果 5000 端口被占用：
```bash
# 查看占用端口的进程
netstat -ano | findstr :5000

# 终止进程（替换 PID）
taskkill /PID <PID> /F
```

**4. 中文编码问题**

如果遇到编码错误，设置环境变量：
```bash
set PYTHONIOENCODING=utf-8
python src\web_app.py
```

或在 PowerShell 中：
```powershell
$env:PYTHONIOENCODING="utf-8"
python src\web_app.py
```

### Windows 推荐工具

- **终端：** Windows Terminal (微软商店免费下载)
- **编辑器：** VS Code + Python 扩展
- **Git：** Git for Windows (https://git-scm.com/download/win)

## 📦 完整依赖列表

### 核心依赖

| 包名 | 版本 | 用途 | 必需 |
|------|------|------|------|
| Flask | 3.0.0 | Web 框架 | ✅ |
| openai | 1.12.0 | API 客户端 | ✅ |
| python-dotenv | 1.0.0 | 环境变量管理 | ✅ |
| requests | 2.31.0 | HTTP 请求 | ✅ |
| duckduckgo-search | 4.1.1 | 网络搜索 | ⚠️ 可选 |

### 测试依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| pytest | 7.4.0 | 测试框架 |
| pytest-cov | 4.1.0 | 覆盖率报告 |

### 安装命令

**安装全部依赖：**
```bash
pip install -r requirements.txt
```

**仅安装核心依赖（不含测试工具）：**
```bash
pip install Flask==3.0.0 openai==1.12.0 python-dotenv==1.0.0 requests==2.31.0
```

**安装测试工具：**
```bash
pip install pytest==7.4.0 pytest-cov==4.1.0
```

---

## 📁 项目结构

```
agent-system/
├── src/
│   ├── agent.py              # 基础对话 Agent
│   ├── agent_with_tools.py   # 支持工具调用
│   ├── complete_agent.py     # 完整版（含搜索/天气/新闻）
│   ├── memory_enhanced.py    # 增强记忆（用户偏好学习）
│   ├── tool_optimizer.py     # 工具调用优化
│   ├── prompt_ab_test.py     # A/B 测试提示词
│   ├── tools.py              # 工具集合（搜索/天气/文件等）
│   ├── memory.py             # 基础记忆模块
│   ├── config.py             # 配置管理
│   └── web_app.py            # Web 界面
├── templates/
│   ├── index.html            # 主界面（带打字动画）
│   ├── index_mobile.html     # 移动端适配
│   └── index_voice.html      # 语音输入版本
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_ab_test.py
├── docs/
│   └── setup_guide.md
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🛠️ 可用工具

| 工具 | 功能 | 示例 |
|------|------|------|
| calculator | 计算器 | "计算 123 * 456" |
| get_current_time | 获取当前时间 | "现在几点了" |
| get_current_date | 获取当前日期 | "今天几号" |
| get_weather | 天气查询 | "北京天气" |
| web_search | 网络搜索 | "搜索 Python 教程" |
| get_news | 获取新闻 | "获取最新新闻" |
| list_files | 列出文件 | "列出当前目录" |
| read_file | 读取文件 | "读取 config.py" |
| write_file | 写入文件 | "保存文件到 test.txt" |
| reminder | 创建提醒 | "提醒我明天开会" |

## 🎯 6 大新增功能

### 1. 打字动画 ✨

消息逐字显示，模拟真实打字效果。

**实现位置：** `templates/index.html`

### 2. 移动端适配 📱

响应式布局，手机/平板友好。

**访问：** http://localhost:5000/mobile

### 3. 语音输入 🎤

支持语音转文字输入。

**访问：** http://localhost:5000 (默认语音版)

**要求：** Chrome 或 Edge 浏览器

### 4. 用户偏好学习 🧠

从对话中自动学习用户偏好。

**查看偏好：** 在 complete_agent 中输入 `prefs`

### 5. 工具调用优化 ⚡

根据使用频率自动优化工具选择。

**查看报告：** 在 agent_with_tools 中输入 `report`

### 6. A/B 测试提示词 🧪

测试不同提示词效果。

**运行测试：** `python src/prompt_ab_test.py`

## 📊 测试

### 运行测试

**运行所有测试：**
```bash
pytest tests/ -v
```

**运行单个测试文件：**
```bash
pytest tests/test_agent.py -v
pytest tests/test_tools.py -v
pytest tests/test_ab_test.py -v
```

**运行特定测试函数：**
```bash
pytest tests/test_agent.py::test_agent_initialization -v
```

### 代码覆盖率

**生成覆盖率报告：**
```bash
# 终端输出
pytest --cov=src tests/

# 生成 HTML 报告（在 htmlcov/ 目录）
pytest --cov=src --cov-report=html tests/

# 生成 XML 报告（用于 CI/CD）
pytest --cov=src --cov-report=xml tests/
```

**查看覆盖率摘要：**
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### 传统测试方式（兼容）

```bash
python tests/test_agent.py
python tests/test_tools.py
python tests/test_ab_test.py
```

## 💰 成本估算

使用阿里云百炼 qwen-plus：
- 价格：¥0.004/千 tokens
- 日常使用：约¥20-50/月

省钱技巧：
- 使用 qwen-turbo（¥0.002/千 tokens）
- 限制回复长度
- 优化提示词

## 🔧 开发

### 添加新工具

1. 在 `src/tools.py` 中添加工具方法
2. 在 `TOOL_REGISTRY` 中注册工具
3. 测试工具功能

### 修改提示词

编辑 `src/agent.py` 中的 `_get_system_prompt()` 方法。

### 自定义 Web 界面

修改 `templates/` 目录下的 HTML 文件。

## 📝 常见问题

### API Key 无效？

检查 `.env` 文件配置，确保 API Key 正确无误。

### 语音输入不工作？

- 使用 Chrome 或 Edge 浏览器
- 允许麦克风权限
- 检查麦克风是否被占用

### 移动端显示异常？

- 清除浏览器缓存
- 使用现代浏览器
- 检查 viewport 设置

## 📚 学习资源

- [7 天搭建 Agent 系统完整攻略](../../guides/agent-system-7days.md)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**Created with ❤️ by You**

Happy Coding! 🚀
