"""
提示词 A/B 测试系统
功能：测试不同提示词效果，记录最佳实践
"""

import json
import os
from datetime import datetime
from openai import OpenAI
import time
from dotenv import load_dotenv

load_dotenv()

class PromptABTester:
    """提示词 A/B 测试器"""
    
    def __init__(self, results_file="ab_test_results.json"):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("API_BASE")
        )
        self.model = os.getenv("MODEL_NAME", "qwen-plus")
        self.results_file = results_file
        self.results = []
        self.load()
        
        # 定义待测试的提示词版本
        self.prompt_versions = {
            "v1_standard": """你是一个友好、乐于助人的 AI 助手。

你的特点：
1. 用中文交流，语气友好自然
2. 回答简洁明了，避免冗长
3. 如果不知道答案，诚实告知
4. 不涉及政治、暴力等敏感话题
5. 不提供医疗、法律等专业建议

请保持对话流畅，像朋友一样交流。""",
            
            "v2_concise": """你是一个简洁高效的 AI 助手。

要求：
- 回答简短，直击要点
- 不说废话
- 只提供必要信息
- 用词精准""",
            
            "v3_detailed": """你是一个详细全面的 AI 助手。

要求：
- 回答详细，提供充分解释
- 给出背景信息和相关上下文
- 必要时提供示例
- 确保信息完整准确""",
            
            "v4_humorous": """你是一个幽默风趣的 AI 助手。

要求：
- 语气轻松有趣
- 适当使用表情符号
- 偶尔讲笑话或调侃
- 让对话充满乐趣"""
        }
    
    def load(self):
        """加载测试结果"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, "r", encoding="utf-8") as f:
                    self.results = json.load(f)
            except:
                self.results = []
    
    def save(self):
        """保存测试结果"""
        with open(self.results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
    
    def run_test(self, test_question, versions=None):
        """运行 A/B 测试"""
        if versions is None:
            versions = list(self.prompt_versions.keys())
        
        print(f"\n🧪 A/B 测试：{test_question}")
        print("=" * 60)
        
        results = []
        
        for version in versions:
            prompt = self.prompt_versions[version]
            
            print(f"\n测试版本：{version}")
            
            start_time = time.time()
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": test_question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                duration = time.time() - start_time
                reply = response.choices[0].message.content
                tokens = response.usage.total_tokens
                
                print(f"✅ 完成（{duration:.2f}秒，{tokens} tokens）")
                
                results.append({
                    "version": version,
                    "response": reply,
                    "duration": duration,
                    "tokens": tokens,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"❌ 失败：{e}")
                results.append({
                    "version": version,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # 保存结果
        self.results.append({
            "question": test_question,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
        
        return results
    
    def analyze_results(self):
        """分析测试结果"""
        if not self.results:
            print("暂无测试数据")
            return
        
        print("\n📊 A/B 测试分析报告")
        print("=" * 60)
        
        # 统计各版本表现
        version_stats = {}
        
        for test in self.results:
            for result in test["results"]:
                version = result["version"]
                
                if version not in version_stats:
                    version_stats[version] = {
                        "count": 0,
                        "total_duration": 0,
                        "total_tokens": 0,
                        "errors": 0
                    }
                
                version_stats[version]["count"] += 1
                
                if "duration" in result:
                    version_stats[version]["total_duration"] += result["duration"]
                    version_stats[version]["total_tokens"] += result["tokens"]
                else:
                    version_stats[version]["errors"] += 1
        
        # 计算平均值
        print(f"\n📈 各版本表现：")
        for version, stats in version_stats.items():
            count = stats["count"]
            avg_duration = stats["total_duration"] / count if count else 0
            avg_tokens = stats["total_tokens"] / count if count else 0
            error_rate = stats["errors"] / count * 100 if count else 0
            
            print(f"\n{version}:")
            print(f"   测试次数：{count}")
            print(f"   平均耗时：{avg_duration:.2f}秒")
            print(f"   平均 tokens: {avg_tokens:.1f}")
            print(f"   错误率：{error_rate:.1f}%")
        
        # 推荐最佳版本
        print(f"\n🏆 推荐版本：")
        if version_stats:
            best_version = min(
                version_stats.items(),
                key=lambda x: (x[1]["total_duration"] / x[1]["count"] if x[1]["count"] else float('inf'))
            )
            print(f"   最快响应：{best_version[0]}")
        
        print("=" * 60)
    
    def get_best_prompt(self):
        """获取最佳提示词"""
        if not self.results:
            return self.prompt_versions["v1_standard"]
        
        # 简单策略：返回最近测试中表现最好的
        self.analyze_results()
        return self.prompt_versions["v1_standard"]  # 简化处理
    
    def clear_results(self):
        """清空测试结果"""
        self.results = []
        self.save()
        print("🧹 测试结果已清空")


if __name__ == "__main__":
    tester = PromptABTester()
    
    print("=" * 60)
    print("🧪 提示词 A/B 测试系统")
    print("=" * 60)
    
    # 运行测试
    test_questions = [
        "你好",
        "解释一下量子力学",
        "推荐一部电影"
    ]
    
    for question in test_questions:
        tester.run_test(question)
    
    # 分析结果
    tester.analyze_results()
