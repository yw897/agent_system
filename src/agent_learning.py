"""
Agent 学习模块
功能：用户偏好学习和应用
"""

from memory_enhanced import EnhancedMemory

class AgentLearning:
    """Agent 学习管理器"""
    
    def __init__(self):
        """初始化学习管理器"""
        self.memory = EnhancedMemory()
        print("🧠 学习系统已启动")
    
    def analyze_preference(self, user_input, response):
        """
        分析用户偏好
        
        Args:
            user_input: 用户输入
            response: AI 响应
        """
        self.memory._analyze_preference(user_input, response)
    
    def learn_from_feedback(self, feedback):
        """
        从反馈中学习
        
        Args:
            feedback: 用户反馈（正面/负面）
        """
        self.memory.learn_from_feedback(feedback)
    
    def get_context(self):
        """获取记忆上下文"""
        return self.memory.get_context()
    
    def get_preferences_summary(self):
        """获取偏好摘要"""
        return self.memory.get_preferences_summary()
    
    def add_to_history(self, user_input, response):
        """添加到对话历史"""
        self.memory.add_to_history(user_input, response)
    
    def show_preferences(self):
        """显示当前学习的偏好"""
        prefs = self.memory.get_preferences_summary()
        print("\n📊 用户偏好分析：")
        print(f"   兴趣话题：{', '.join(prefs.get('topics', [])) or '未检测'}")
        print(f"   回复风格：{prefs.get('response_style', '未设定')}")
        print(f"   常用工具：{', '.join(prefs.get('favorite_tools', [])) or '未使用'}")
        print(f"   活跃时段：{prefs.get('active_hours', [])}")
    
    def get_style_instruction(self):
        """获取风格指导"""
        prefs = self.memory.get_preferences_summary()
        style_map = {
            "简洁": "回答要简洁明了，避免冗长，直击要点。",
            "详细": "回答要详细全面，提供充分解释和背景信息。",
            "幽默": "回答要幽默风趣，适当使用表情符号和玩笑。",
            "专业": "回答要专业严谨，使用准确术语。"
        }
        return style_map.get(prefs.get("response_style"), "")
