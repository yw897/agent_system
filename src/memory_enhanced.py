"""
增强记忆模块
功能：持久化存储 + 用户偏好学习
"""

import json
import os
from datetime import datetime

class EnhancedMemory:
    """增强记忆管理类"""
    
    def __init__(self, memory_file="memory.json", preferences_file="user_preferences.json"):
        self.memory_file = memory_file
        self.preferences_file = preferences_file
        self.data = {
            "facts": [],
            "preferences": [],
            "history": []
        }
        self.preferences = {
            "topics": [],          # 感兴趣的话题
            "response_style": "",  # 回复风格（简洁/详细/幽默等）
            "favorite_tools": [],  # 常用工具
            "active_hours": []     # 活跃时间段
        }
        self.load()
    
    def load(self):
        """加载记忆和偏好"""
        # 加载记忆
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
        
        # 加载偏好
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r", encoding="utf-8") as f:
                    self.preferences = json.load(f)
                print(f"💾 已加载偏好文件：{self.preferences_file}")
            except Exception as e:
                print(f"⚠️ 加载偏好失败：{e}")
        else:
            print("📝 创建新的偏好文件")
            self.save_preferences()
    
    def save(self):
        """保存记忆到文件"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存记忆失败：{e}")
    
    def save_preferences(self):
        """保存偏好到文件"""
        try:
            with open(self.preferences_file, "w", encoding="utf-8") as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存偏好失败：{e}")
    
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
        
        # ✨ 自动分析用户偏好
        self._analyze_preference(user_input, response)
    
    def _analyze_preference(self, user_input, response):
        """分析用户偏好（简化版）"""
        input_lower = user_input.lower()
        
        # 检测感兴趣的话题
        topic_keywords = {
            "科技": ["科技", "技术", "AI", "人工智能", "编程", "代码", "python", "开发"],
            "生活": ["生活", "日常", "吃饭", "睡觉", "运动", "健康"],
            "工作": ["工作", "会议", "项目", "任务", "报告"],
            "娱乐": ["电影", "音乐", "游戏", "笑话", "娱乐", "电视剧"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in input_lower for kw in keywords):
                if topic not in self.preferences["topics"]:
                    self.preferences["topics"].append(topic)
                    print(f"🎯 检测到用户兴趣：{topic}")
                    self.save_preferences()
        
        # 检测回复风格偏好
        if len(user_input) < 10:
            # 用户喜欢简短输入，可能偏好简洁回复
            if self.preferences["response_style"] != "简洁":
                self.preferences["response_style"] = "简洁"
                print(f"🎯 检测到用户偏好：简洁回复")
                self.save_preferences()
        
        # 记录活跃时间
        hour = datetime.now().hour
        if hour not in self.preferences["active_hours"]:
            self.preferences["active_hours"].append(hour)
            self.preferences["active_hours"].sort()
            self.save_preferences()
    
    def learn_from_feedback(self, user_input, feedback):
        """从用户反馈中学习"""
        if "太长了" in feedback or "简洁点" in feedback or "简单点" in feedback:
            self.preferences["response_style"] = "简洁"
            print("🎯 学习：用户偏好简洁回复")
            self.save_preferences()
        
        if "详细点" in feedback or "多解释" in feedback or "详细些" in feedback:
            self.preferences["response_style"] = "详细"
            print("🎯 学习：用户偏好详细回复")
            self.save_preferences()
        
        if "好笑" in feedback or "幽默" in feedback or "有趣" in feedback:
            self.preferences["response_style"] = "幽默"
            print("🎯 学习：用户偏好幽默风格")
            self.save_preferences()
    
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
        """获取记忆上下文（用于提示词）"""
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
        
        # ✨ 添加用户偏好
        if self.preferences["topics"]:
            context += f"\n用户兴趣：{', '.join(self.preferences['topics'])}\n"
        
        if self.preferences["response_style"]:
            context += f"回复风格：{self.preferences['response_style']}\n"
        
        return context if len(context) > 10 else ""
    
    def get_preferences_summary(self):
        """获取偏好总结"""
        return self.preferences


if __name__ == "__main__":
    memory = EnhancedMemory()
    
    print("🧪 测试增强记忆系统")
    print("-" * 30)
    
    memory.add_to_history("我喜欢科技新闻", "好的，我会多关注科技方面的内容")
    memory.add_to_history("简洁点", "好的")
    memory.learn_from_feedback("", "太长了，简洁点")
    
    print("\n📋 当前偏好：")
    print(memory.get_preferences_summary())
