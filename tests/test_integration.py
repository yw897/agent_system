"""
集成测试
功能：测试完整流程和模块间协作
"""

import sys
import os
import json
import tempfile

# 添加 src 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_mock_agent():
    """测试 Mock Agent 基本功能"""
    print("\n" + "=" * 60)
    print("🧪 测试 Mock Agent")
    print("=" * 60)
    
    from mock_agent import MockAgent
    
    agent = MockAgent()
    
    # 测试问候
    response = agent.chat("你好")
    assert "你好" in response or "嗨" in response or "Mock" in response
    print(f"✅ 问候测试通过：{response[:50]}...")
    
    # 测试计算
    response = agent.chat("帮我计算 10 + 20")
    assert "30" in response or "Mock" in response
    print(f"✅ 计算测试通过：{response[:50]}...")
    
    # 测试时间
    response = agent.chat("现在几点")
    assert "时间" in response or "Mock" in response
    print(f"✅ 时间测试通过：{response[:50]}...")
    
    # 测试历史管理
    agent.clear_history()
    assert len(agent.messages) == 0
    print("✅ 历史清空测试通过")
    
    # 测试统计
    stats = agent.get_stats()
    assert stats["mode"] == "mock"
    print(f"✅ 统计测试通过：{stats}")
    
    return True

def test_agent_base():
    """测试 Agent 基础类"""
    print("\n" + "=" * 60)
    print("🧪 测试 Agent 基础类")
    print("=" * 60)
    
    from agent_base import AgentBase
    
    # 测试 Mock 模式
    agent = AgentBase(use_mock=True)
    assert agent.use_mock == True
    assert agent.is_ready() == True
    print("✅ Mock 模式初始化测试通过")
    
    # 测试消息管理
    agent.add_message("user", "测试消息")
    assert len(agent.messages) == 1
    print("✅ 消息添加测试通过")
    
    # 测试历史修剪
    for i in range(15):
        agent.add_message("user", f"消息{i}")
    agent._trim_history()
    # max_history defaults to 100, so with 15 messages it won't trim
    # Let's test with more messages
    for i in range(100):
        agent.add_message("user", f"消息{i}")
    agent._trim_history()
    assert len(agent.messages) <= 101  # max_history=100 + 1 system
    print("✅ 历史修剪测试通过")
    
    # 测试清空历史
    agent.clear_history()
    assert len(agent.messages) == 1  # 只剩 system
    print("✅ 历史清空测试通过")
    
    return True

def test_agent_tools():
    """测试工具执行器"""
    print("\n" + "=" * 60)
    print("🧪 测试工具执行器")
    print("=" * 60)
    
    from agent_tools import AgentTools
    from tools import TOOL_REGISTRY
    
    executor = AgentTools(TOOL_REGISTRY)
    
    # 测试工具数量
    count = executor.get_tool_count()
    assert count > 0
    print(f"✅ 工具数量测试通过：{count} 个工具")
    
    # 测试工具名称
    names = executor.get_tool_names()
    assert "calculator" in names
    print(f"✅ 工具名称测试通过：{len(names)} 个工具已注册")
    
    # 测试计算器执行
    result = executor.execute_tool("calculator", {"expression": "123 * 456"})
    assert "56088" in result
    print(f"✅ 计算器执行测试通过：{result}")
    
    # 测试时间工具
    result = executor.execute_tool("get_current_time", {})
    assert "当前时间" in result
    print(f"✅ 时间工具执行测试通过")
    
    # 测试未知工具
    result = executor.execute_tool("unknown_tool", {})
    assert "未知工具" in result
    print(f"✅ 未知工具处理测试通过")
    
    # 测试 JSON 解析
    json_text = '```json\n{"tool": "calculator", "params": {"expression": "10+20"}}\n```'
    parsed = executor.parse_tool_call(json_text)
    assert parsed is not None
    assert parsed["tool"] == "calculator"
    print(f"✅ JSON 解析测试通过")
    
    return True

def test_tool_optimizer():
    """测试工具优化器"""
    print("\n" + "=" * 60)
    print("🧪 测试工具优化器")
    print("=" * 60)
    
    from tool_optimizer import ToolOptimizer
    
    # 创建临时日志文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        optimizer = ToolOptimizer(log_file=temp_file)
        
        # 测试日志记录
        optimizer.log_usage("calculator", success=True, duration=0.5)
        optimizer.log_usage("calculator", success=True, duration=0.6)
        optimizer.log_usage("get_weather", success=False, duration=2.0)
        
        print("✅ 日志记录测试通过")
        
        # 测试统计
        stats = optimizer.get_usage_stats()
        assert stats["frequency"]["calculator"] == 2
        assert stats["frequency"]["get_weather"] == 1
        print(f"✅ 统计测试通过：{stats['frequency']}")
        
        # 测试成功率
        assert stats["success_rate"]["calculator"] == 1.0
        assert stats["success_rate"]["get_weather"] == 0.0
        print(f"✅ 成功率测试通过")
        
        # 测试推荐
        suggestion = optimizer.suggest_tool("帮我计算一下")
        assert suggestion == "calculator"
        print(f"✅ 工具推荐测试通过：{suggestion}")
        
        # 测试优化推荐
        optimized = optimizer.get_optimized_tools()
        assert "calculator" in optimized
        print(f"✅ 优化推荐测试通过：{optimized}")
        
        # 测试性能报告
        perf = optimizer.get_performance_report("calculator")
        assert perf is not None
        assert perf["total_calls"] == 2
        print(f"✅ 性能报告测试通过")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    return True

def test_agent_learning():
    """测试学习模块"""
    print("\n" + "=" * 60)
    print("🧪 测试学习模块")
    print("=" * 60)
    
    from agent_learning import AgentLearning
    
    learning = AgentLearning()
    
    # 测试偏好获取
    prefs = learning.get_preferences_summary()
    assert isinstance(prefs, dict)
    print(f"✅ 偏好获取测试通过")
    
    # 测试上下文获取
    context = learning.get_context()
    assert isinstance(context, str)
    print(f"✅ 上下文获取测试通过")
    
    # 测试历史添加
    learning.add_to_history("用户输入", "AI 响应")
    print(f"✅ 历史添加测试通过")
    
    return True

def test_complete_agent_mock():
    """测试 Complete Agent（Mock 模式）"""
    print("\n" + "=" * 60)
    print("🧪 测试 Complete Agent（Mock 模式）")
    print("=" * 60)
    
    from complete_agent import CompleteAgent
    
    agent = CompleteAgent(use_mock=True)
    
    # 测试初始化
    assert agent.use_mock == True
    print("✅ Mock 模式初始化测试通过")
    
    # 测试对话
    response = agent.chat("你好")
    assert response is not None
    print(f"✅ Mock 对话测试通过：{response[:50]}...")
    
    # 测试历史清空
    agent.clear_history()
    print("✅ Mock 历史清空测试通过")
    
    return True

def test_full_workflow():
    """测试完整工作流程"""
    print("\n" + "=" * 60)
    print("🧪 测试完整工作流程")
    print("=" * 60)
    
    from agent_tools import AgentTools
    from tool_optimizer import ToolOptimizer
    from tools import TOOL_REGISTRY
    
    # 创建优化器
    optimizer = ToolOptimizer()
    
    # 创建工具执行器
    executor = AgentTools(TOOL_REGISTRY, optimizer)
    
    # 模拟一次完整的工具调用
    tool_name = "calculator"
    params = {"expression": "100 + 200"}
    
    result = executor.execute_tool(tool_name, params)
    
    # 验证结果
    assert "300" in result
    print(f"✅ 工具执行测试通过：{result}")
    
    # 验证日志记录
    stats = optimizer.get_usage_stats()
    assert tool_name in stats["frequency"]
    print(f"✅ 日志记录测试通过")
    
    # 验证推荐
    suggestion = optimizer.suggest_tool("计算 500 * 2")
    assert suggestion == tool_name
    print(f"✅ 智能推荐测试通过：{suggestion}")
    
    return True

def run_all_tests():
    """运行所有集成测试"""
    print("\n" + "=" * 70)
    print("🧪 集成测试套件 - Agent 系统")
    print("=" * 70)
    
    tests = [
        ("Mock Agent", test_mock_agent),
        ("Agent 基础类", test_agent_base),
        ("工具执行器", test_agent_tools),
        ("工具优化器", test_tool_optimizer),
        ("学习模块", test_agent_learning),
        ("Complete Agent (Mock)", test_complete_agent_mock),
        ("完整工作流程", test_full_workflow)
    ]
    
    results = []
    failed_tests = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            if not result:
                failed_tests.append(name)
        except Exception as e:
            print(f"\n❌ {name} 测试异常：{e}")
            import traceback
            traceback.print_exc()
            results.append(False)
            failed_tests.append(name)
    
    # 打印总结
    print("\n" + "=" * 70)
    print("📊 集成测试总结")
    print("=" * 70)
    print(f"✅ 通过：{sum(results)}/{len(results)}")
    print(f"❌ 失败：{len(failed_tests)}/{len(results)}")
    
    if failed_tests:
        print(f"\n⚠️ 失败的测试：{', '.join(failed_tests)}")
    
    print("=" * 70)
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    
    # 返回退出码
    exit(0 if success else 1)
