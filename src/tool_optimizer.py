"""
工具调用优化器
功能：分析工具使用频率，自动优化调用策略
增强版本：添加缓存、性能分析、智能推荐
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

class ToolOptimizer:
    """工具调用优化器 - 增强版"""
    
    def __init__(self, log_file="tool_usage_log.json"):
        """
        初始化工具优化器
        
        Args:
            log_file: 日志文件路径
        """
        self.log_file = log_file
        self.usage_log = []
        self.cache = {}  # 简单缓存
        self.load()
    
    def load(self):
        """加载使用日志"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    self.usage_log = json.load(f)
            except:
                self.usage_log = []
    
    def save(self):
        """保存使用日志"""
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.usage_log, f, ensure_ascii=False, indent=2)
    
    def log_usage(self, tool_name, success=True, duration=0, user_intent=None):
        """
        记录工具使用
        
        Args:
            tool_name: 工具名称
            success: 是否成功
            duration: 执行耗时（秒）
            user_intent: 用户意图（可选）
        """
        log_entry = {
            "tool": tool_name,
            "success": success,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "intent": user_intent
        }
        
        self.usage_log.append(log_entry)
        
        # 只保留最近 1000 条
        if len(self.usage_log) > 1000:
            self.usage_log = self.usage_log[-1000:]
        
        self.save()
    
    def get_usage_stats(self, days=None):
        """
        获取使用统计
        
        Args:
            days: 统计最近 N 天的数据（None 表示全部）
            
        Returns:
            dict: 统计数据
        """
        if not self.usage_log:
            return {}
        
        # 时间过滤
        logs = self.usage_log
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            logs = [
                log for log in logs 
                if datetime.fromisoformat(log["timestamp"]) > cutoff
            ]
        
        if not logs:
            return {}
        
        # 工具使用频率
        tool_counts = Counter([log["tool"] for log in logs])
        
        # 成功率
        tool_success = {}
        for tool in tool_counts.keys():
            tool_logs = [log for log in logs if log["tool"] == tool]
            success_count = sum(1 for log in tool_logs if log["success"])
            tool_success[tool] = success_count / len(tool_logs) if tool_logs else 0
        
        # 平均响应时间
        tool_duration = {}
        for tool in tool_counts.keys():
            tool_logs = [log for log in logs if log["tool"] == tool]
            durations = [log["duration"] for log in tool_logs if log["duration"] > 0]
            tool_duration[tool] = sum(durations) / len(durations) if durations else 0
        
        # 按时间段统计（小时）
        hourly_usage = defaultdict(int)
        for log in logs:
            hour = datetime.fromisoformat(log["timestamp"]).hour
            hourly_usage[hour] += 1
        
        return {
            "frequency": dict(tool_counts),
            "success_rate": tool_success,
            "avg_duration": tool_duration,
            "hourly_usage": dict(hourly_usage),
            "total_logs": len(logs)
        }
    
    def get_optimized_tools(self, limit=5, days=None):
        """
        获取推荐工具（基于使用频率和成功率）
        
        Args:
            limit: 返回数量限制
            days: 统计最近 N 天的数据
            
        Returns:
            list: 推荐工具列表
        """
        stats = self.get_usage_stats(days=days)
        
        if not stats:
            return []
        
        # 计算综合得分
        tool_scores = []
        for tool, count in stats["frequency"].items():
            success_rate = stats["success_rate"].get(tool, 0)
            avg_duration = stats["avg_duration"].get(tool, 1)
            
            # 综合得分 = 频率 * 成功率 / 响应时间
            score = (count * success_rate) / max(avg_duration, 0.1)
            tool_scores.append((tool, score))
        
        # 按得分排序
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [tool for tool, score in tool_scores[:limit]]
    
    def suggest_tool(self, user_intent):
        """
        根据用户意图推荐工具
        
        Args:
            user_intent: 用户输入/意图
            
        Returns:
            str: 推荐的工具名称
        """
        # 意图关键词映射
        intent_keywords = {
            "calculator": ["计算", "数学", "加减乘除", "等于", "算一下", "*", "/", "+", "-"],
            "get_weather": ["天气", "气温", "下雨", "晴天", "多少度", "冷", "热"],
            "web_search": ["搜索", "查询", "找一下", "看看", "查一下", "了解"],
            "get_news": ["新闻", "时事", "最新消息", "头条", "热点"],
            "get_current_time": ["时间", "几点", "时钟", "现在"],
            "get_current_date": ["日期", "几号", "星期", "今天", "明天"],
            "list_files": ["文件", "目录", "列出", "文件夹", "查看文件"],
            "read_file": ["读取", "打开文件", "查看内容", "读文件"],
            "write_file": ["保存", "写入", "创建文件", "写文件", "记录"]
        }
        
        # 统计匹配的工具
        tool_matches = {}
        for tool, keywords in intent_keywords.items():
            matches = sum(1 for kw in keywords if kw in user_intent.lower())
            if matches > 0:
                tool_matches[tool] = matches
        
        if not tool_matches:
            return None
        
        # 获取优化工具列表
        optimized = self.get_optimized_tools()
        
        # 优先推荐优化过的工具
        for opt_tool in optimized:
            if opt_tool in tool_matches:
                return opt_tool
        
        # 否则返回匹配度最高的
        return max(tool_matches, key=tool_matches.get)
    
    def get_performance_report(self, tool_name):
        """
        获取单个工具的性能报告
        
        Args:
            tool_name: 工具名称
            
        Returns:
            dict: 性能报告
        """
        tool_logs = [log for log in self.usage_log if log["tool"] == tool_name]
        
        if not tool_logs:
            return None
        
        total = len(tool_logs)
        success = sum(1 for log in tool_logs if log["success"])
        durations = [log["duration"] for log in tool_logs if log["duration"] > 0]
        
        return {
            "tool": tool_name,
            "total_calls": total,
            "success_count": success,
            "fail_count": total - success,
            "success_rate": success / total if total > 0 else 0,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.cache = {}
    
    def clear_log(self):
        """清空日志"""
        self.usage_log = []
        self.save()
        print("🧹 工具使用日志已清空")
    
    def export_stats(self, output_file="tool_stats.json"):
        """
        导出统计数据到文件
        
        Args:
            output_file: 输出文件路径
        """
        stats = self.get_usage_stats()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"📊 统计数据已导出到：{output_file}")
    
    def print_report(self):
        """打印使用报告"""
        stats = self.get_usage_stats()
        
        print("\n📊 工具使用报告")
        print("=" * 60)
        
        if not stats:
            print("暂无使用记录")
            return
        
        print(f"📈 总使用次数：{stats.get('total_logs', 0)}")
        
        print(f"\n📈 使用频率 TOP 5:")
        sorted_freq = sorted(stats["frequency"].items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (tool, count) in enumerate(sorted_freq, 1):
            print(f"   {i}. {tool}: {count} 次")
        
        print(f"\n✅ 成功率:")
        for tool, rate in stats["success_rate"].items():
            emoji = "✅" if rate >= 0.9 else "⚠️" if rate >= 0.7 else "❌"
            print(f"   {emoji} {tool}: {rate*100:.1f}%")
        
        print(f"\n⚡ 平均响应时间:")
        for tool, duration in stats["avg_duration"].items():
            print(f"   {tool}: {duration:.2f}秒")
        
        print(f"\n🎯 推荐工具（综合得分）:")
        optimized = self.get_optimized_tools(5)
        for i, tool in enumerate(optimized, 1):
            print(f"   {i}. {tool}")
        
        print(f"\n📅 活跃时段分布:")
        hourly = stats.get("hourly_usage", {})
        if hourly:
            peak_hour = max(hourly, key=hourly.get)
            print(f"   高峰时段：{peak_hour}:00-{peak_hour+1}:00")
        
        print("=" * 60)


if __name__ == "__main__":
    optimizer = ToolOptimizer()
    
    # 模拟日志
    print("📝 生成模拟数据...")
    for i in range(20):
        optimizer.log_usage("calculator", success=True, duration=0.5 + i * 0.01)
    
    for i in range(15):
        optimizer.log_usage("get_weather", success=True, duration=1.2 + i * 0.02)
    
    for i in range(5):
        optimizer.log_usage("web_search", success=False if i == 2 else True, duration=2.0 + i * 0.1)
    
    optimizer.print_report()
    
    # 测试推荐
    print("\n💡 意图识别测试:")
    test_cases = [
        "帮我计算 123 * 456",
        "北京天气怎么样",
        "搜索一下 Python 教程",
        "今天有什么新闻"
    ]
    
    for test in test_cases:
        suggestion = optimizer.suggest_tool(test)
        print(f"   '{test}' → {suggestion}")
    
    # 测试性能报告
    print("\n📊 工具性能报告:")
    perf = optimizer.get_performance_report("calculator")
    if perf:
        print(f"   工具：{perf['tool']}")
        print(f"   总调用：{perf['total_calls']} 次")
        print(f"   成功率：{perf['success_rate']*100:.1f}%")
        print(f"   平均耗时：{perf['avg_duration']:.2f}秒")
