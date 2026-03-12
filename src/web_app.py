"""
Web 应用 - Flask 版本
功能：通过浏览器访问 Agent，支持打字动画、语音输入、移动端适配
"""

from flask import Flask, render_template, request, jsonify
from complete_agent import CompleteAgent

app = Flask(__name__)
agent = CompleteAgent()

@app.route("/")
def index():
    """主页 - 使用语音版本（包含打字动画和移动端适配）"""
    return render_template("index_voice.html")

@app.route("/mobile")
def mobile():
    """移动端专用页面"""
    return render_template("index_mobile.html")

@app.route("/chat", methods=["POST"])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        message = data.get("message", "")
        
        if not message:
            return jsonify({"response": "请输入消息"})
        
        response = agent.chat(message)
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"response": f"❌ 错误：{str(e)}"})

@app.route("/clear", methods=["POST"])
def clear():
    """清空对话历史"""
    try:
        agent.clear_history()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/prefs", methods=["GET"])
def prefs():
    """获取用户偏好"""
    try:
        prefs = agent.memory.get_preferences_summary()
        return jsonify(prefs)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 Web 服务启动中...")
    print("=" * 60)
    print("访问地址：http://localhost:5000")
    print("💡 移动端访问：http://localhost:5000/mobile")
    print("💡 语音版本：http://localhost:5000 (默认)")
    print("按 Ctrl+C 停止服务")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000, host="0.0.0.0")
