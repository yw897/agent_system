"""
配置管理模块
功能：统一管理 API 配置和系统参数
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # API 配置
    API_KEY = os.getenv("API_KEY", "")
    API_BASE = os.getenv("API_BASE", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen-plus")
    
    # 模型参数
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    # 系统配置
    DEBUG = True
    MEMORY_FILE = "memory.json"
    MAX_HISTORY = 100  # 最大对话历史条数
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        errors = []
        
        if not cls.API_KEY:
            errors.append("API_KEY 未配置")
        
        if not cls.API_BASE:
            errors.append("API_BASE 未配置")
        
        return errors
    
    @classmethod
    def print_info(cls):
        """打印配置信息（隐藏敏感数据）"""
        print("📋 当前配置：")
        print(f"   API_BASE: {cls.API_BASE}")
        print(f"   MODEL_NAME: {cls.MODEL_NAME}")
        print(f"   TEMPERATURE: {cls.TEMPERATURE}")
        print(f"   MAX_TOKENS: {cls.MAX_TOKENS}")
        if cls.API_KEY:
            key_preview = cls.API_KEY[:8] + "..." if len(cls.API_KEY) > 8 else cls.API_KEY
            print(f"   API_KEY: {key_preview} ✓")

if __name__ == "__main__":
    Config.print_info()
    
    errors = Config.validate()
    if errors:
        print("\n❌ 配置错误：")
        for error in errors:
            print(f"   - {error}")
    else:
        print("\n✅ 配置验证通过")
