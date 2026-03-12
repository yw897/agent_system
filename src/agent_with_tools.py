"""
支持工具调用的 Agent
功能：解析工具调用请求，执行工具，返回结果
"""

import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("❌ 错误：未安装 openai 库")
    print("请运行：pip install openai")
    exit(1)

from memory import Memory
from tools import TOOL_REGISTRY, get_tool_description

load_dotenv()

class AgentWithTools:
    """支持工具调用的 Agent"""
    
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
            
            self.memory = Memory()
            self.messages = [
                {"role": "system", "content": self._get_system_prompt()}
            ]
            self.tools = TOOL_REGISTRY
            
            print(f"🤖 Agent with Tools 初始化完成")
            print(f"   模型：{self.model}")
            print(f"   可用工具：{len(self.tools)} 个")
            
        except Exception as e:
            print(f"❌ 创建客户端失败：{e}")
            self.client = None
    
    def _get_system_prompt(self):
        """生成包含工具信息的系统提示词"""
        tools_desc = get_tool_description()
        context = self.memory.get_context()
        
        return f"""你是一个智能助手，可以调用工具帮助用户完成任务。

{context}

## 可用工具：
{tools_desc}

## 工具调用格式：
当需要调用工具时，请严格按以下 JSON 格式回复（不要添加其他内容）：

```json
{{
    "tool": "工具名称",
    "params": {{
        "参数名": "参数值"
    }}
}}
```

## 注意事项：
1. 只在确实需要时调用工具
2. 确保参数完整且正确
3. 如果工具执行失败，告知用户并尝试其他方式
4. 不需要工具时，直接自然语言回复

请保持友好、专业的态度。"""
    
    def _parse_tool_call(self, text):
        """解析工具调用请求"""
        # 尝试从代码块中提取 JSON
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = text
        
        try:
            tool_call = json.loads(json_str)
            if "tool" in tool_call:
                return tool_call
        except json.JSONDecodeError:
            pass
        except Exception:
            pass
        
        return None
    
    def _execute_tool(self, tool_name, params):
        """执行工具"""
        if tool_name not in self.tools:
            return f"❌ 未知工具：{tool_name}"
        
        tool_info = self.tools[tool_name]
        func = tool_info["func"]
        
        try:
            result = func(**params)
            return result
        except TypeError as e:
            return f"❌ 参数错误：{e}"
        except Exception as e:
            return f"❌ 执行失败：{e}"
    
    def chat(self, user_input):
        """处理用户输入（支持工具调用）"""
        if self.client is None:
            return "❌ Agent 未初始化，请检查配置"
        
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            # 第一次调用大模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
            # 检查是否需要调用工具
            tool_call = self._parse_tool_call(assistant_message)
            
            if tool_call:
                tool_name = tool_call.get("tool")
                params = tool_call.get("params", {})
                
                if tool_name:
                    print(f"🔧 调用工具：{tool_name}")
                    
                    # 执行工具
                    tool_result = self._execute_tool(tool_name, params)
                    
                    # 添加工具调用记录
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    self.messages.append({
                        "role": "user",
                        "content": f"工具 '{tool_name}' 执行结果：\n{tool_result}"
                    })
                    
                    # 第二次调用大模型，整合结果
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens
                    )
                    
                    final_response = response.choices[0].message.content
                    
                    # 保存对话历史
                    self.memory.add_to_history(user_input, final_response)
                    self.messages.append({
                        "role": "assistant",
                        "content": final_response
                    })
                    
                    self._trim_history()
                    
                    return final_response
            
            # 不需要工具，直接回复
            self.messages.append({"role": "assistant", "content": assistant_message})
            self.memory.add_to_history(user_input, assistant_message)
            self._trim_history()
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"抱歉，遇到了一些问题：{str(e)}"
            self.messages.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def _trim_history(self):
        """修剪对话历史"""
        max_history = 100
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
    agent = AgentWithTools()
    
    if agent.client is None:
        print("\n❌ 无法启动对话，请检查配置")
        return
    
    print("\n" + "=" * 50)
    print("🤖 Agent with Tools 已启动！")
    print("=" * 50)
    print("💡 可用工具示例：")
    print("   - 计算：123 * 456")
    print("   - 时间：现在几点了")
    print("   - 文件：列出当前目录文件")
    print("   - 提醒：提醒我明天开会")
    print("   - 天气：北京天气")
    print("   - 搜索：搜索 Python 教程")
    print("\n输入 'quit' 退出，'clear' 清空历史")
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
