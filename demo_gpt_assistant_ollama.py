#!/usr/bin/env python3
"""
GPT Assistant with Ollama Demo
Demo cho GPT Assistant sử dụng Ollama model
"""

import sys
import os
sys.path.append('src')

from src.ai.gpt_assistant import GPTAssistant

def test_ollama_connection():
    """Test Ollama connection"""
    print("🔧 Test kết nối Ollama...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama đang chạy!")
            models = response.json().get("models", [])
            print(f"📦 Models có sẵn: {len(models)}")
            for model in models[:5]:  # Show first 5 models
                print(f"   - {model.get('name', 'Unknown')}")
            return True
        else:
            print("❌ Ollama không phản hồi")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối Ollama: {e}")
        print("\n🔧 Hướng dẫn:")
        print("1. Cài đặt Ollama: https://ollama.ai")
        print("2. Chạy: ollama serve")
        print("3. Tải model: ollama pull llama2:7b")
        print("4. Fine-tune: python scripts/finetune_gpt_assistant.py")
        return False

def demo_gpt_assistant_ollama():
    """Demo GPT Assistant với Ollama"""
    print("🤖 GPT Assistant với Ollama Demo")
    print("=" * 50)
    
    # Initialize GPT Assistant with Ollama
    print("🚀 Khởi tạo GPT Assistant với Ollama...")
    gpt_assistant = GPTAssistant(model_name="gpt_assistant:latest")
    
    # Test questions
    test_questions = [
        "RSI là gì?",
        "MACD hoạt động như thế nào?",
        "Bollinger Bands dùng để làm gì?",
        "Sharpe Ratio quan trọng như thế nào?",
        "Làm thế nào để quản lý rủi ro?",
        "Có nên timing thị trường không?",
        "Làm thế nào để xây dựng portfolio?",
        "Phân tích cơ bản là gì?",
        "Phân tích kỹ thuật là gì?",
        "Đầu tư giá trị là gì?"
    ]
    
    print("\n🔍 **Demo: Hỏi đáp với Ollama**")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Câu hỏi: {question}")
        print("-" * 40)
        
        try:
            analysis = gpt_assistant.analyze_question(question)
            response = gpt_assistant.format_response(analysis)
            print(f"Loại: {analysis.get('type', 'unknown')}")
            print(f"Độ tin cậy: {analysis.get('confidence', 0):.1%}")
            if 'source' in analysis:
                print(f"Nguồn: {analysis['source']}")
            if 'model_version' in analysis:
                print(f"Model: {analysis['model_version']}")
            print(f"Trả lời:\n{response}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Test indicator explanations
    print("\n📚 **Demo: Giải thích chỉ báo với Ollama**")
    print("=" * 50)
    
    indicators = ["RSI", "MACD", "Bollinger Bands", "Moving Averages"]
    
    for indicator in indicators:
        print(f"\n📊 Giải thích: {indicator}")
        print("-" * 40)
        
        try:
            explanation = gpt_assistant.explain_indicator(indicator)
            if 'error' in explanation:
                print(f"❌ {explanation['error']}")
            else:
                print(f"Tên: {explanation.get('name', 'N/A')}")
                print(f"Mô tả: {explanation.get('description', 'N/A')}")
                if 'source' in explanation:
                    print(f"Nguồn: {explanation['source']}")
                if 'model_version' in explanation:
                    print(f"Model: {explanation['model_version']}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Test investment tips
    print("\n💡 **Demo: Lời khuyên đầu tư với Ollama**")
    print("=" * 50)
    
    topics = ["general", "technical", "risk"]
    
    for topic in topics:
        print(f"\n💡 Lời khuyên về: {topic}")
        print("-" * 40)
        
        try:
            tips = gpt_assistant.get_investment_tips(topic)
            for i, tip in enumerate(tips, 1):
                print(f"{i}. {tip}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo GPT Assistant với Ollama hoàn thành!")
    print("=" * 50)
    
    print("\n💡 **So sánh với GPT Assistant cũ:**")
    print("✅ Sử dụng AI thông minh thay vì hard-coded")
    print("✅ Hiểu context tốt hơn")
    print("✅ Trả lời chi tiết và chính xác hơn")
    print("✅ Có thể fine-tuning thêm")
    print("✅ Chạy local, không cần internet")

def main():
    """Main function"""
    print("🤖 GPT Assistant với Ollama Demo")
    print("=" * 40)
    
    # Test Ollama connection first
    if not test_ollama_connection():
        print("\n⚠️ Ollama chưa sẵn sàng!")
        print("Hãy cài đặt và fine-tune model trước:")
        print("1. python scripts/finetune_gpt_assistant.py")
        print("2. python demo_gpt_assistant_ollama.py")
        return
    
    # Run demo
    demo_gpt_assistant_ollama()

if __name__ == "__main__":
    main() 