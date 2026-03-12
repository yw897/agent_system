"""
基础 Agent 类
功能：实现多轮对话，维护对话历史
"""

import os
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("❌ 错误：未安装 openai 库")
    print("请运行：pip install openai")
    exit(1)

load_dotenv()

class SimpleAgent:
    """简单 Agent 类 - 支持多轮对话"""
    
    def __init__(self):
        """初始化 Agent"""
        api_key = os.getenv("API_KEY")
        base_url = os.getenv("API_BASE")
        
        if not api_key:
            print("❌ 错误：未找到 API_KEY，请检查 .env 文件")
            self.client = None
            return
        
        if not base_url:
            print("❌ 错误：未找到 API_BASE，请检查 .env 文件")
            self.client = None
            return
        
        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            self.model = os.getenv("MODEL_NAME", "qwen-plus")
            self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
            self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
            
            self.messages = [
                {"role": "system", "content": self._get_system_prompt()}
            ]
            
            print(f"🤖 Agent 初始化完成，使用模型：{self.model}")
            
        except Exception as e:
            print(f"❌ 创建客户端失败：{e}")
            self.client = None
    
    def _get_system_prompt(self):
        """获取系统提示词"""
        return """你是一个友好、乐于助人的 AI 助手。

你的特点：
1. 用中文交流，语气友好自然
2. 回答简洁明了，避免冗长
3. 如果不知道答案，诚实告知
4. 不涉及政治、暴力等敏感话题
5. 不提供医疗、法律等专业建议

请保持对话流畅，像朋友一样交流。"""
    
    def chat(self, user_input):
        """处理用户输入，返回 AI 回复"""
        if self.client is None:
            return "❌ Agent 未初始化，请检查配置"
        
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
            self.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            self._trim_history()
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"抱歉，遇到了一些问题：{str(e)}"
            self.messages.append({
                "role": "assistant",
                "content": error_msg
            })
            return error_msg
    
    def _trim_history(self):
        """修剪对话历史"""
        max_history = int(os.getenv("MAX_HISTORY", "100"))
        
        if len(self.messages) > max_history + 1:
            self.messages = [self.messages[0]] + self.messages[-max_history:]
    
    def clear_history(self):
        """清空对话历史"""
        self.messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]
        print("🧹 对话历史已清空")


def interactive_chat():
    """启动交互式对话"""
    agent = SimpleAgent()
    
    if agent.client is None:
        print("\n❌ 无法启动对话，请检查配置")
        return
    
    print("\n" + "=" * 50)
    print("🤖 Agent 已启动！")
    print("=" * 50)
    print("💡 提示：")
    print("   - 输入任意文字与 AI 对话")
    print("   - 输入 'clear' 清空对话历史")
    print("   - 输入 'quit' 或 'exit' 退出")
    print("=" * 50 + "\n")
    
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
