"""
Agent 基础类
功能：提供 Agent 核心功能（对话管理、历史维护、配置）
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use environment variables directly

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class AgentBase:
    """Agent 基础类 - 提供核心对话功能"""
    
    def __init__(self, use_mock=False):
        """
        初始化 Agent
        
        Args:
            use_mock: 是否使用 Mock 模式
        """
        self.use_mock = use_mock
        self.messages = []
        self.client = None
        self.model = None
        self.temperature = None
        self.max_tokens = None
        
        if not use_mock:
            self._init_client()
    
    def _init_client(self):
        """初始化 API 客户端"""
        api_key = os.getenv("API_KEY")
        base_url = os.getenv("API_BASE")
        
        if not api_key:
            print("❌ 错误：未找到 API_KEY，请检查 .env 文件或设置 MOCK_MODE=true")
            return
        
        if not base_url:
            print("❌ 错误：未找到 API_BASE，请检查 .env 文件")
            return
        
        if OpenAI is None:
            print("❌ 错误：未安装 openai 库，请运行：pip install openai")
            return
        
        try:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = os.getenv("MODEL_NAME", "qwen-plus")
            self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
            self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
            print(f"🤖 Agent 初始化完成，使用模型：{self.model}")
        except Exception as e:
            print(f"❌ 创建客户端失败：{e}")
    
    def _get_system_prompt(self):
        """获取系统提示词 - 子类可重写"""
        return """你是一个友好、乐于助人的 AI 助手。

你的特点：
1. 用中文交流，语气友好自然
2. 回答简洁明了，避免冗长
3. 如果不知道答案，诚实告知
4. 不涉及政治、暴力等敏感话题
5. 不提供医疗、法律等专业建议

请保持对话流畅，像朋友一样交流。"""
    
    def add_message(self, role, content):
        """添加消息到对话历史"""
        self.messages.append({"role": role, "content": content})
    
    def _trim_history(self):
        """修剪对话历史"""
        max_history = int(os.getenv("MAX_HISTORY", "100"))
        if len(self.messages) > max_history + 1:
            self.messages = [self.messages[0]] + self.messages[-max_history:]
    
    def clear_history(self):
        """清空对话历史"""
        self.messages = [{"role": "system", "content": self._get_system_prompt()}]
        print("🧹 对话历史已清空")
    
    def get_message_count(self):
        """获取消息数量"""
        return len(self.messages)
    
    def is_ready(self):
        """检查 Agent 是否就绪"""
        if self.use_mock:
            return True
        return self.client is not None
