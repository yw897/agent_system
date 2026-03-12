"""
Agent 测试模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_agent_initialization():
    """测试 Agent 初始化"""
    print("\n🧪 测试 Agent 初始化...")
    try:
        from agent import SimpleAgent
        agent = SimpleAgent()
        print("✅ Agent 初始化成功")
        return True
    except Exception as e:
        print(f"❌ Agent 初始化失败：{e}")
        return False

def test_agent_chat():
    """测试对话功能"""
    print("\n🧪 测试对话功能...")
    try:
        from agent import SimpleAgent
        agent = SimpleAgent()
        response = agent.chat("你好")
        if response and len(response) > 0:
            print(f"✅ 对话功能正常，回复：{response[:50]}...")
            return True
        else:
            print("❌ 对话功能返回空响应")
            return False
    except Exception as e:
        print(f"❌ 对话功能测试失败：{e}")
        return False

def test_agent_with_tools():
    """测试工具调用 Agent"""
    print("\n🧪 测试工具调用 Agent...")
    try:
        from agent_with_tools import AgentWithTools
        agent = AgentWithTools()
        print("✅ 工具调用 Agent 初始化成功")
        return True
    except Exception as e:
        print(f"❌ 工具调用 Agent 初始化失败：{e}")
        return False

def test_complete_agent():
    """测试完整版 Agent"""
    print("\n🧪 测试完整版 Agent...")
    try:
        from complete_agent import CompleteAgent
        agent = CompleteAgent()
        print("✅ 完整版 Agent 初始化成功")
        return True
    except Exception as e:
        print(f"❌ 完整版 Agent 初始化失败：{e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Agent 系统测试套件")
    print("=" * 60)
    
    tests = [
        test_agent_initialization,
        test_agent_chat,
        test_agent_with_tools,
        test_complete_agent
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
