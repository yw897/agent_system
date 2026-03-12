"""
完整版 Agent
功能：集成所有功能（搜索/天气/新闻/记忆/工具优化）
重构版本：使用模块化设计
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from agent_base import AgentBase
from agent_tools import AgentTools
from agent_learning import AgentLearning
from tools import TOOL_REGISTRY, get_tool_description
from tool_optimizer import ToolOptimizer

class CompleteAgent(AgentBase):
    """完整版 Agent - 包含所有增强功能"""
    
    def __init__(self, use_mock=False):
        """
        初始化 Complete Agent
        
        Args:
            use_mock: 是否使用 Mock 模式
        """
        super().__init__(use_mock=use_mock)
        
        if use_mock:
            print("🎭 Mock 模式已启用")
            return
        
        # 学习系统
        self.learning = AgentLearning()
        
        # 工具执行器
        self.optimizer = ToolOptimizer()
        self.tool_executor = AgentTools(TOOL_REGISTRY, self.optimizer)
        
        # 初始化系统提示
        self.messages = [{"role": "system", "content": self._get_system_prompt()}]
        
        print(f"🤖 Complete Agent 初始化完成")
        print(f"   模型：{self.model}")
        print(f"   工具：{self.tool_executor.get_tool_count()} 个")
        print(f"   学习系统：已启动")
        print(f"   优化器：已启动")
    
    def _get_system_prompt(self):
        """生成包含偏好信息的系统提示词"""
        if self.use_mock:
            return "你是一个智能助手（Mock 模式）。"
        
        tools_desc = get_tool_description()
        context = self.learning.get_context()
        prefs = self.learning.get_preferences_summary()
        
        style_instruction = self.learning.get_style_instruction()
        
        return f"""你是一个智能助手，可以调用工具帮助用户完成任务。

{context}

## 可用工具：
{tools_desc}

## 工具调用格式：
当需要调用工具时，请严格按以下 JSON 格式回复：

```json
{{
    "tool": "工具名称",
    "params": {{
        "参数名": "参数值"
    }}
}}
```

{style_instruction}

## 注意事项：
1. 只在确实需要时调用工具
2. 确保参数完整且正确
3. 如果工具执行失败，告知用户并尝试其他方式
4. 不需要工具时，直接自然语言回复

请保持友好、专业的态度。"""
    
    def chat(self, user_input):
        """
        处理用户输入
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            str: AI 响应
        """
        if self.use_mock:
            from mock_agent import MockAgent
            mock = MockAgent()
            return mock.chat(user_input)
        
        if not self.is_ready():
            return "❌ Agent 未初始化，请检查配置或使用 Mock 模式"
        
        # 智能推荐工具
        suggested_tool = self.optimizer.suggest_tool(user_input)
        if suggested_tool:
            print(f"💡 推荐工具：{suggested_tool}")
        
        # 添加用户消息
        self.add_message("user", user_input)
        
        # 调用 API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        assistant_message = response.choices[0].message.content
        tool_call = self.tool_executor.parse_tool_call(assistant_message)
        
        # 处理工具调用
        if tool_call:
            tool_name = tool_call.get("tool")
            params = tool_call.get("params", {})
            
            if tool_name:
                print(f"🔧 调用工具：{tool_name}")
                
                tool_result = self.tool_executor.execute_tool(tool_name, params)
                
                self.add_message("assistant", assistant_message)
                self.add_message("user", f"工具 '{tool_name}' 执行结果：\n{tool_result}")
                
                # 获取最终响应
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                final_response = response.choices[0].message.content
                
                # 学习和记忆
                self.learning.add_to_history(user_input, final_response)
                self.add_message("assistant", final_response)
                
                self._trim_history()
                
                return final_response
        
        # 无工具调用
        self.add_message("assistant", assistant_message)
        self.learning.add_to_history(user_input, assistant_message)
        self._trim_history()
        
        return assistant_message
    
    def show_preferences(self):
        """显示当前学习的偏好"""
        if self.use_mock:
            print("ℹ️ Mock 模式下偏好学习已禁用")
            return
        self.learning.show_preferences()
    
    def show_optimizer_report(self):
        """显示工具优化报告"""
        if self.use_mock:
            print("ℹ️ Mock 模式下优化器已禁用")
            return
        self.optimizer.print_report()


def interactive_chat():
    """启动交互式对话"""
    # 检查是否启用 Mock 模式
    use_mock = os.getenv("MOCK_MODE", "false").lower() == "true"
    
    agent = CompleteAgent(use_mock=use_mock)
    
    if not agent.is_ready() and not use_mock:
        print("\n❌ 无法启动对话，请检查配置或设置 MOCK_MODE=true")
        return
    
    print("\n" + "=" * 60)
    mode_str = "🎭 Mock 模式" if use_mock else "🤖 真实模式"
    print(f"{mode_str} 已启动！")
    print("=" * 60)
    
    if not use_mock:
        print("💡 我会从对话中学习你的偏好，越用越懂你")
        print("💡 输入 'prefs' 查看当前学习的偏好")
        print("💡 输入 'report' 查看工具使用报告")
    
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
            
            if user_input.lower() == "prefs":
                agent.show_preferences()
                continue
            
            if user_input.lower() == "report":
                agent.show_optimizer_report()
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
