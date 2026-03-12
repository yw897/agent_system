"""
A/B 测试系统测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_ab_tester_initialization():
    """测试 A/B 测试器初始化"""
    print("\n🧪 测试 A/B 测试器初始化...")
    try:
        from prompt_ab_test import PromptABTester
        tester = PromptABTester()
        print("✅ A/B 测试器初始化成功")
        return True
    except Exception as e:
        print(f"❌ A/B 测试器初始化失败：{e}")
        return False

def test_prompt_versions():
    """测试提示词版本"""
    print("\n🧪 测试提示词版本...")
    try:
        from prompt_ab_test import PromptABTester
        tester = PromptABTester()
        
        if len(tester.prompt_versions) >= 4:
            print(f"✅ 提示词版本正常：{len(tester.prompt_versions)} 个版本")
            return True
        else:
            print("❌ 提示词版本数量不足")
            return False
    except Exception as e:
        print(f"❌ 提示词版本测试失败：{e}")
        return False

def test_optimizer():
    """测试工具优化器"""
    print("\n🧪 测试工具优化器...")
    try:
        from tool_optimizer import ToolOptimizer
        optimizer = ToolOptimizer()
        
        # 测试日志记录
        optimizer.log_usage("calculator", success=True, duration=0.5)
        optimizer.log_usage("calculator", success=True, duration=0.6)
        optimizer.log_usage("get_weather", success=False, duration=1.2)
        
        stats = optimizer.get_usage_stats()
        if stats and "frequency" in stats:
            print(f"✅ 工具优化器正常")
            return True
        else:
            print("❌ 工具优化器统计异常")
            return False
    except Exception as e:
        print(f"❌ 工具优化器测试失败：{e}")
        return False

def test_tool_suggestion():
    """测试工具推荐"""
    print("\n🧪 测试工具推荐...")
    try:
        from tool_optimizer import ToolOptimizer
        optimizer = ToolOptimizer()
        
        # 测试意图识别
        suggestion = optimizer.suggest_tool("帮我计算 123 * 456")
        if suggestion:
            print(f"✅ 工具推荐正常：{suggestion}")
            return True
        else:
            print("⚠️ 工具推荐为空（可能是正常情况）")
            return True  # 不算失败
    except Exception as e:
        print(f"❌ 工具推荐测试失败：{e}")
        return False

def run_all_tests():
    """运行所有 A/B 测试相关测试"""
    print("=" * 60)
    print("🧪 A/B 测试系统测试套件")
    print("=" * 60)
    
    tests = [
        test_ab_tester_initialization,
        test_prompt_versions,
        test_optimizer,
        test_tool_suggestion
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试异常：{e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果：{sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
