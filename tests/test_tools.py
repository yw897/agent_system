"""
工具模块测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_calculator():
    """测试计算器"""
    print("\n🧪 测试计算器...")
    from tools import Tools
    
    result = Tools.calculator("123 * 456")
    if "56088" in result:
        print(f"✅ 计算器正常：123 * 456 = 56088")
        return True
    else:
        print(f"❌ 计算器异常：{result}")
        return False

def test_time():
    """测试时间获取"""
    print("\n🧪 测试时间获取...")
    from tools import Tools
    
    result = Tools.get_current_time()
    if "当前时间" in result:
        print(f"✅ 时间获取正常：{result}")
        return True
    else:
        print(f"❌ 时间获取异常：{result}")
        return False

def test_date():
    """测试日期获取"""
    print("\n🧪 测试日期获取...")
    from tools import Tools
    
    result = Tools.get_current_date()
    if "今天日期" in result:
        print(f"✅ 日期获取正常：{result}")
        return True
    else:
        print(f"❌ 日期获取异常：{result}")
        return False

def test_list_files():
    """测试文件列表"""
    print("\n🧪 测试文件列表...")
    from tools import Tools
    
    result = Tools.list_files(".")
    if "目录" in result or "文件" in result:
        print(f"✅ 文件列表正常")
        return True
    else:
        print(f"❌ 文件列表异常：{result}")
        return False

def test_reminder():
    """测试提醒功能"""
    print("\n🧪 测试提醒功能...")
    from tools import Tools
    
    result = Tools.reminder("测试提醒")
    if "提醒已创建" in result:
        print(f"✅ 提醒功能正常")
        return True
    else:
        print(f"❌ 提醒功能异常：{result}")
        return False

def run_all_tests():
    """运行所有工具测试"""
    print("=" * 60)
    print("🧪 工具模块测试套件")
    print("=" * 60)
    
    tests = [
        test_calculator,
        test_time,
        test_date,
        test_list_files,
        test_reminder
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
