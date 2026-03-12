"""
工具模块
功能：提供各种可调用工具的实现
"""

import os
import re
from datetime import datetime

# 尝试导入网络搜索库（可选）
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("⚠️  duckduckgo-search 未安装，网络搜索功能不可用")
    print("   安装：pip install duckduckgo-search")

# 尝试导入 requests（用于天气查询）
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class Tools:
    """工具集合类"""
    
    @staticmethod
    def calculator(expression):
        """计算器工具"""
        try:
            # 安全检查：只允许数字和基本运算符
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in expression):
                return "❌ 错误：表达式包含非法字符"
            
            # 检查空表达式
            if not expression.strip():
                return "❌ 错误：表达式为空"
            
            result = eval(expression)
            return f"✅ 计算结果：{result}"
            
        except ZeroDivisionError:
            return "❌ 错误：除数不能为零"
        except SyntaxError:
            return "❌ 错误：表达式语法错误"
        except Exception as e:
            return f"❌ 计算错误：{e}"
    
    @staticmethod
    def get_current_time():
        """获取当前时间"""
        now = datetime.now()
        return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"
    
    @staticmethod
    def get_current_date():
        """获取当前日期"""
        now = datetime.now()
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[now.weekday()]
        return f"今天日期：{now.strftime('%Y年%m月%d日')} {weekday}"
    
    @staticmethod
    def reminder(content, remind_time=None):
        """创建提醒"""
        timestamp = datetime.now().isoformat()
        reminder_text = f"[{timestamp}] 提醒：{content}"
        
        try:
            with open("reminders.txt", "a", encoding="utf-8") as f:
                f.write(reminder_text + "\n")
            return f"✅ 提醒已创建：{content}"
        except Exception as e:
            return f"❌ 创建提醒失败：{e}"
    
    @staticmethod
    def read_file(filepath):
        """读取文件"""
        try:
            # 安全检查：不允许路径遍历
            if ".." in filepath:
                return "❌ 错误：不允许使用相对路径"
            
            if not os.path.exists(filepath):
                return f"❌ 错误：文件不存在：{filepath}"
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 限制文件大小
            if len(content) > 2000:
                content = content[:2000] + "\n...（内容过长，已截断）"
            
            return f"📄 文件内容：\n{content}"
            
        except UnicodeDecodeError:
            return "❌ 错误：无法读取文件（非文本文件）"
        except Exception as e:
            return f"❌ 读取失败：{e}"
    
    @staticmethod
    def write_file(filepath, content):
        """写入文件"""
        try:
            # 安全检查：不允许路径遍历
            if ".." in filepath:
                return "❌ 错误：不允许使用相对路径"
            
            # 创建目录（如果需要）
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            return f"✅ 文件已保存：{filepath}"
            
        except Exception as e:
            return f"❌ 保存失败：{e}"
    
    @staticmethod
    def list_files(directory="."):
        """列出目录内容"""
        try:
            # 安全检查：不允许路径遍历
            if ".." in directory:
                return "❌ 错误：不允许使用相对路径"
            
            if not os.path.exists(directory):
                return f"❌ 错误：目录不存在：{directory}"
            
            items = os.listdir(directory)
            files = []
            dirs = []
            
            for item in items:
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    dirs.append(f"📁 {item}/")
                else:
                    files.append(f"📄 {item}")
            
            result = f"📂 目录：{directory}\n\n"
            if dirs:
                result += "目录：\n" + "\n".join(dirs) + "\n\n"
            if files:
                result += "文件：\n" + "\n".join(files)
            
            return result
            
        except Exception as e:
            return f"❌ 列出失败：{e}"
    
    @staticmethod
    def web_search(query, max_results=5):
        """网络搜索工具（使用 DuckDuckGo）"""
        if not DDGS_AVAILABLE:
            return "❌ 错误：未安装 duckduckgo-search，请运行：pip install duckduckgo-search"
        
        try:
            results = DDGS().text(query, max_results=max_results)
            
            if not results:
                return f"未找到关于'{query}'的相关信息"
            
            formatted = []
            for i, r in enumerate(results, 1):
                item = f"{i}. {r.get('title', '无标题')}\n"
                item += f"   链接：{r.get('href', '')}\n"
                item += f"   摘要：{r.get('body', '')}\n"
                formatted.append(item)
            
            header = f"🔍 搜索结果（关于'{query}'）：\n\n"
            return header + "\n".join(formatted)
            
        except Exception as e:
            return f"❌ 搜索失败：{e}"
    
    @staticmethod
    def get_weather(city):
        """天气查询工具（使用 wttr.in）"""
        if not REQUESTS_AVAILABLE:
            return "❌ 错误：未安装 requests 库"
        
        try:
            # 使用英文城市名以提高准确性
            url = f"https://wttr.in/{city}?format=%C+%t+%h+%w"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                weather_data = response.text.strip()
                return f"🌤️ {city} 天气：{weather_data}"
            else:
                return f"❌ 天气查询失败，状态码：{response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ 天气查询超时，请稍后重试"
        except requests.exceptions.ConnectionError:
            return "❌ 天气查询失败：网络连接错误"
        except Exception as e:
            return f"❌ 天气查询错误：{e}"
    
    @staticmethod
    def get_news(category="top", limit=5):
        """获取新闻工具"""
        if not DDGS_AVAILABLE:
            return "❌ 错误：未安装 duckduckgo-search"
        
        try:
            query = f"news {category}" if category != "top" else "latest news"
            results = DDGS().news(query, max_results=limit)
            
            if not results:
                return f"未找到{category}相关新闻"
            
            formatted = []
            for i, r in enumerate(results, 1):
                item = f"{i}. {r.get('title', '无标题')}\n"
                item += f"   来源：{r.get('source', '')}\n"
                item += f"   时间：{r.get('date', '')}\n"
                item += f"   链接：{r.get('url', '')}\n"
                formatted.append(item)
            
            header = f"📰 最新新闻（{category}）：\n\n"
            return header + "\n".join(formatted)
            
        except Exception as e:
            return f"❌ 获取新闻失败：{e}"


# 工具注册表
TOOL_REGISTRY = {
    "calculator": {
        "description": "计算器，用于数学计算",
        "func": Tools.calculator,
        "params": {"expression": "数学表达式，如 '123 + 456'"}
    },
    "get_current_time": {
        "description": "获取当前时间",
        "func": Tools.get_current_time,
        "params": {}
    },
    "get_current_date": {
        "description": "获取当前日期",
        "func": Tools.get_current_date,
        "params": {}
    },
    "reminder": {
        "description": "创建提醒事项",
        "func": Tools.reminder,
        "params": {"content": "提醒内容", "remind_time": "提醒时间（可选）"}
    },
    "read_file": {
        "description": "读取文件内容",
        "func": Tools.read_file,
        "params": {"filepath": "文件路径"}
    },
    "write_file": {
        "description": "写入文件",
        "func": Tools.write_file,
        "params": {"filepath": "文件路径", "content": "文件内容"}
    },
    "list_files": {
        "description": "列出目录内容",
        "func": Tools.list_files,
        "params": {"directory": "目录路径（默认当前目录）"}
    },
    "web_search": {
        "description": "网络搜索，查询最新信息",
        "func": Tools.web_search,
        "params": {
            "query": "搜索关键词",
            "max_results": "最大结果数（默认 5）"
        }
    },
    "get_weather": {
        "description": "查询指定城市的天气",
        "func": Tools.get_weather,
        "params": {"city": "城市名，如'北京'或'Beijing'"}
    },
    "get_news": {
        "description": "获取最新新闻",
        "func": Tools.get_news,
        "params": {
            "category": "新闻类别（top/world/business/technology）",
            "limit": "新闻条数（默认 5）"
        }
    }
}


def get_tool_description():
    """获取所有工具的描述文本"""
    descriptions = []
    for name, info in TOOL_REGISTRY.items():
        params_str = ", ".join([f"{k}: {v}" for k, v in info["params"].items()])
        desc = f"- {name}: {info['description']}"
        if params_str:
            desc += f" (参数：{params_str})"
        descriptions.append(desc)
    
    return "\n".join(descriptions)


if __name__ == "__main__":
    print("🧪 测试工具模块")
    print("=" * 50)
    
    print("\n1. 测试计算器：")
    print(Tools.calculator("123 * 456"))
    
    print("\n2. 测试获取时间：")
    print(Tools.get_current_time())
    
    print("\n3. 测试获取日期：")
    print(Tools.get_current_date())
    
    print("\n4. 测试列出文件：")
    print(Tools.list_files("."))
    
    print("\n5. 测试创建提醒：")
    print(Tools.reminder("测试提醒"))
    
    print("\n6. 可用工具列表：")
    print(get_tool_description())
