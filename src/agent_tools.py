"""
Agent 工具执行模块
功能：处理工具调用和执行
"""

import json
import re
from datetime import datetime

class AgentTools:
    """Agent 工具执行器"""
    
    def __init__(self, tool_registry, optimizer=None):
        """
        初始化工具执行器
        
        Args:
            tool_registry: 工具注册表
            optimizer: 工具优化器（可选）
        """
        self.tools = tool_registry
        self.optimizer = optimizer
    
    def parse_tool_call(self, text):
        """
        解析工具调用请求
        
        Args:
            text: AI 响应文本
            
        Returns:
            dict: 工具调用信息，格式 {"tool": "工具名", "params": {...}}
        """
        # 尝试提取 JSON
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        json_str = match.group(1) if match else text
        
        try:
            tool_call = json.loads(json_str)
            if "tool" in tool_call:
                return tool_call
        except:
            pass
        
        return None
    
    def execute_tool(self, tool_name, params):
        """
        执行工具
        
        Args:
            tool_name: 工具名称
            params: 工具参数
            
        Returns:
            str: 执行结果
        """
        if tool_name not in self.tools:
            return f"❌ 未知工具：{tool_name}"
        
        tool_info = self.tools[tool_name]
        func = tool_info["func"]
        
        start_time = datetime.now()
        
        try:
            result = func(**params)
            
            # 记录使用日志
            duration = (datetime.now() - start_time).total_seconds()
            if self.optimizer:
                self.optimizer.log_usage(tool_name, success=True, duration=duration)
            
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            if self.optimizer:
                self.optimizer.log_usage(tool_name, success=False, duration=duration)
            return f"❌ 执行失败：{e}"
    
    def get_tool_names(self):
        """获取所有工具名称"""
        return list(self.tools.keys())
    
    def get_tool_count(self):
        """获取工具数量"""
        return len(self.tools)
