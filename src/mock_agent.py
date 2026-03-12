"""
Mock Agent - 用于无 API Key 时测试核心功能
功能：模拟 API 响应，便于测试和开发
"""

import os
import json
import random
from datetime import datetime

class MockAgent:
    """Mock Agent - 模拟 API 响应"""
    
    def __init__(self):
        """初始化 Mock Agent"""
        self.messages = []
        self.mock_responses = self._load_mock_responses()
        print("🎭 Mock Agent 已启动（无 API 调用模式）")
    
    def _load_mock_responses(self):
        """加载预设的 Mock 响应"""
        return {
            "greeting": [
                "你好！我是你的 AI 助手，有什么可以帮你的吗？",
                "嗨！很高兴见到你，今天想聊些什么？",
                "你好呀！我随时准备帮助你～"
            ],
            "calculator": "计算结果是：{result}",
            "time": "当前时间是 {time}",
            "default": [
                "这是一个 Mock 响应。在真实模式下，我会调用 AI API 来回答你的问题。",
                "Mock 模式测试中... 功能正常！",
                "✅ 测试通过：对话流程正常工作"
            ]
        }
    
    def chat(self, user_input):
        """处理用户输入，返回 Mock 响应"""
        self.messages.append({"role": "user", "content": user_input})
        
        # 检测用户意图并返回相应的 Mock 响应
        response = self._generate_mock_response(user_input)
        
        self.messages.append({"role": "assistant", "content": response})
        self._trim_history()
        
        return response
    
    def _generate_mock_response(self, user_input):
        """根据用户输入生成 Mock 响应"""
        user_lower = user_input.lower()
        
        # 问候语
        if any(word in user_lower for word in ["你好", "嗨", "hello", "hi"]):
            return random.choice(self.mock_responses["greeting"])
        
        # 计算相关
        if any(word in user_lower for word in ["计算", "算", "+", "-", "*", "/"]):
            # 尝试简单计算
            try:
                # 安全检查：只允许数字和基本运算符
                expr = user_lower.replace("计算", "").replace("算一下", "").strip()
                if all(c in "0123456789+-*/(). " for c in expr):
                    result = eval(expr)
                    return f"计算结果是：{result}"
            except:
                pass
            return "计算结果是：[Mock 结果]"
        
        # 时间相关
        if any(word in user_lower for word in ["时间", "几点", "clock"]):
            return f"当前时间是 {datetime.now().strftime('%H:%M:%S')}"
        
        # 日期相关
        if any(word in user_lower for word in ["日期", "几号", "星期", "date"]):
            now = datetime.now()
            weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
            return f"今天是 {now.year}年{now.month}月{now.day}日 {weekdays[now.weekday()]}"
        
        # 工具调用测试
        if "工具" in user_lower or "tool" in user_lower:
            return "Mock 工具调用测试：✅ 工具系统正常工作"
        
        # 记忆功能测试
        if "记忆" in user_lower or "memory" in user_lower:
            return "Mock 记忆功能测试：✅ 记忆系统正常工作"
        
        # 默认响应
        return random.choice(self.mock_responses["default"])
    
    def _trim_history(self):
        """修剪对话历史"""
        max_history = 10
        if len(self.messages) > max_history:
            self.messages = self.messages[-max_history:]
    
    def clear_history(self):
        """清空对话历史"""
        self.messages = []
        print("🧹 Mock 对话历史已清空")
    
    def get_stats(self):
        """获取统计信息"""
        return {
            "total_messages": len(self.messages),
            "mode": "mock",
            "api_calls": 0
        }


def interactive_chat():
    """启动交互式 Mock 对话"""
    agent = MockAgent()
    
    print("\n" + "=" * 60)
    print("🎭 Mock Agent 已启动！")
    print("=" * 60)
    print("💡 这是 Mock 模式 - 不需要 API Key")
    print("💡 用于测试核心功能和对话流程")
    print("💡 输入 'quit' 退出，'clear' 清空历史")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("👤 你：").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 再见！")
                break
            
            if user_input.lower() == "clear":
                agent.clear_history()
                continue
            
            if not user_input:
                continue
            
            response = agent.chat(user_input)
            print(f"🤖 AI：{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}\n")


if __name__ == "__main__":
    interactive_chat()
