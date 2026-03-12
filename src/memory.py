"""
记忆模块
功能：持久化存储对话历史和重要信息
"""

import json
import os
from datetime import datetime

class Memory:
    """记忆管理类"""
    
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.data = {
            "facts": [],
            "preferences": [],
            "history": []
        }
        self.load()
    
    def load(self):
        """从文件加载记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                print(f"💾 已加载记忆文件：{self.memory_file}")
            except Exception as e:
                print(f"⚠️ 加载记忆失败：{e}")
                self.data = {"facts": [], "preferences": [], "history": []}
        else:
            print("📝 创建新的记忆文件")
            self.save()
    
    def save(self):
        """保存记忆到文件"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存记忆失败：{e}")
    
    def add_fact(self, fact):
        """添加事实记忆"""
        self.data["facts"].append({
            "content": fact,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
        print(f"✅ 记住：{fact}")
    
    def add_preference(self, pref):
        """添加用户偏好"""
        self.data["preferences"].append({
            "content": pref,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
        print(f"✅ 记住偏好：{pref}")
    
    def add_to_history(self, user_input, response):
        """添加对话历史"""
        self.data["history"].append({
            "user": user_input,
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制历史记录数量
        if len(self.data["history"]) > 100:
            self.data["history"] = self.data["history"][-100:]
        
        self.save()
    
    def get_facts(self, limit=5):
        """获取最近的事实记忆"""
        return self.data["facts"][-limit:]
    
    def get_preferences(self, limit=5):
        """获取最近的偏好记忆"""
        return self.data["preferences"][-limit:]
    
    def get_recent_history(self, limit=10):
        """获取最近的对话历史"""
        return self.data["history"][-limit:]
    
    def clear(self):
        """清空所有记忆"""
        self.data = {"facts": [], "preferences": [], "history": []}
        self.save()
        print("🧹 所有记忆已清空")
    
    def get_context(self):
        """获取记忆上下文"""
        context = "【已知信息】\n"
        
        facts = self.get_facts(5)
        if facts:
            context += "事实：\n"
            for fact in facts:
                context += f"- {fact['content']}\n"
        
        prefs = self.get_preferences(5)
        if prefs:
            context += "偏好：\n"
            for pref in prefs:
                context += f"- {pref['content']}\n"
        
        return context if len(context) > 10 else ""


if __name__ == "__main__":
    print("🧪 测试记忆系统")
    print("-" * 30)
    
    # 使用测试文件
    memory = Memory(memory_file="test_memory.json")
    
    memory.add_fact("用户喜欢喝咖啡")
    memory.add_preference("用户偏好简洁的回答")
    memory.add_to_history("你好", "你好！有什么可以帮助你的？")
    
    print("\n📋 当前上下文：")
    print(memory.get_context())
    
    print("\n📋 最近历史：")
    for item in memory.get_recent_history(3):
        print(f"  用户：{item['user']}")
        print(f"  AI: {item['assistant']}")
    
    # 清理测试文件
    if os.path.exists("test_memory.json"):
        os.remove("test_memory.json")
        print("\n🧹 测试文件已清理")
