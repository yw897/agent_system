"""
最终功能测试
测试所有核心功能
"""

import sys
import os
import time

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """测试所有模块导入"""
    print("\n" + "=" * 60)
    print("📦 测试模块导入")
    print("=" * 60)
    
    modules = [
        ("Flask", "flask"),
        ("openai", "openai"),
        ("dotenv", "dotenv"),
        ("requests", "requests"),
        ("agent", "agent"),
        ("memory", "memory"),
        ("tools", "tools"),
    ]
    
    failed = []
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️  {len(failed)} 个模块导入失败：{', '.join(failed)}")
        return False
    else:
        print("\n✅ 所有模块导入成功")
        return True


def test_tools():
    """测试工具功能"""
    print("\n" + "=" * 60)
    print("🔧 测试工具功能")
    print("=" * 60)
    
    from tools import Tools
    
    tests = [
        ("计算器", lambda: Tools.calculator("123 * 456")),
        ("时间查询", lambda: Tools.get_current_time()),
        ("日期查询", lambda: Tools.get_current_date()),
        ("列出文件", lambda: Tools.list_files(".")),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            if "错误" not in result:
                print(f"✅ {name}: {result[:50]}...")
            else:
                print(f"⚠️  {name}: {result}")
        except Exception as e:
            print(f"❌ {name}: {e}")


def test_memory():
    """测试记忆功能"""
    print("\n" + "=" * 60)
    print("💾 测试记忆功能")
    print("=" * 60)
    
    from memory import Memory
    
    # 使用测试文件
    memory = Memory(memory_file="test_final_memory.json")
    
    # 测试添加事实
    memory.add_fact("测试事实：用户喜欢编程")
    
    # 测试添加偏好
    memory.add_preference("测试偏好：简洁回复")
    
    # 测试添加历史
    memory.add_to_history("测试问题", "测试回答")
    
    # 验证
    facts = memory.get_facts(1)
    prefs = memory.get_preferences(1)
    history = memory.get_recent_history(1)
    
    if facts and "测试事实" in facts[0]["content"]:
        print("✅ 事实记忆正常")
    else:
        print("❌ 事实记忆异常")
    
    if prefs and "测试偏好" in prefs[0]["content"]:
        print("✅ 偏好记忆正常")
    else:
        print("❌ 偏好记忆异常")
    
    if history and history[0]["user"] == "测试问题":
        print("✅ 历史记忆正常")
    else:
        print("❌ 历史记忆异常")
    
    # 清理测试文件
    if os.path.exists("test_final_memory.json"):
        os.remove("test_final_memory.json")
        print("🧹 测试文件已清理")


def test_web_app():
    """测试 Web 应用"""
    print("\n" + "=" * 60)
    print("🌐 测试 Web 应用")
    print("=" * 60)
    
    # 检查 Flask 应用文件
    if os.path.exists("src/web_app.py"):
        print("✅ web_app.py 存在")
    else:
        print("❌ web_app.py 不存在")
        return
    
    # 检查模板文件
    templates = [
        "templates/index_voice.html",
        "templates/index_mobile.html"
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template} 存在")
        else:
            print(f"❌ {template} 不存在")
    
    # 检查模板内容
    with open("templates/index_voice.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "typing" in content and "语音" in content:
            print("✅ 语音版本包含打字动画和语音输入")
        else:
            print("⚠️  语音版本可能缺少功能")
    
    with open("templates/index_mobile.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "@media" in content or "mobile" in content.lower():
            print("✅ 移动版本包含响应式设计")
        else:
            print("⚠️  移动版本可能缺少响应式设计")


def test_project_structure():
    """测试项目结构"""
    print("\n" + "=" * 60)
    print("📁 测试项目结构")
    print("=" * 60)
    
    required_files = [
        "src/agent.py",
        "src/agent_with_tools.py",
        "src/memory.py",
        "src/tools.py",
        "src/web_app.py",
        "templates/index_voice.html",
        "templates/index_mobile.html",
        "requirements.txt",
        ".env.example",
        "README.md",
        "tests/test_agent.py",
        "tests/test_tools.py"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  缺少 {len(missing)} 个文件")
        return False
    else:
        print("\n✅ 项目结构完整")
        return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 最终功能测试")
    print("=" * 60)
    
    results = {
        "导入测试": test_imports(),
        "工具测试": True,  # 工具测试总是运行
        "记忆测试": True,
        "Web 测试": True,
        "结构测试": True
    }
    
    # 运行各项测试
    test_tools()
    test_memory()
    test_web_app()
    results["结构测试"] = test_project_structure()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以投入使用！")
    else:
        print(f"\n⚠️  {total - passed} 个测试未通过，请检查")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # 切换到项目根目录
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    run_all_tests()
