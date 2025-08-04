#!/usr/bin/env python3
"""
FinGPT Model Demo
Test the custom FinGPT model for Vietnamese financial analysis
"""

import sys
import os
sys.path.append('src')

from src.ai.fingpt_model import FinGPTModel

def demo_fingpt_model():
    """Demo FinGPT model functionality"""
    print("🤖 FinGPT Model Demo")
    print("=" * 50)
    
    # Initialize FinGPT model
    print("🚀 Khởi tạo FinGPT Model...")
    fingpt = FinGPTModel(model_name="fingpt:latest")
    
    # Test questions
    test_questions = [
        "RSI là gì?",
        "MACD hoạt động như thế nào?",
        "Bollinger Bands dùng để làm gì?",
        "Sharpe Ratio quan trọng như thế nào?",
        "Có nên đầu tư vào VNM không?",
        "Thị trường Việt Nam có đặc điểm gì?",
        "Làm thế nào để quản lý rủi ro?"
    ]
    
    print("\n🔍 **Demo: Hỏi đáp FinGPT**")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Câu hỏi: {question}")
        print("-" * 40)
        
        try:
            response = fingpt.ask(question)
            print(f"🤖 **Trả lời:**")
            print(f"Độ tin cậy: {response.confidence:.1%}")
            print(f"Nguồn: {response.source}")
            print(f"Model: {response.model_version}")
            print(f"Nội dung: {response.answer}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Test indicator explanations
    print("\n📚 **Demo: Giải thích chỉ báo**")
    print("=" * 50)
    
    indicators = ["RSI", "MACD", "Bollinger Bands", "Moving Averages"]
    
    for indicator in indicators:
        print(f"\n📊 Giải thích: {indicator}")
        print("-" * 40)
        
        try:
            response = fingpt.explain_indicator(indicator)
            print(f"Độ tin cậy: {response.confidence:.1%}")
            print(f"Nguồn: {response.source}")
            print(f"Nội dung:\n{response.answer}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Test investment tips
    print("\n💡 **Demo: Lời khuyên đầu tư**")
    print("=" * 50)
    
    topics = ["general", "technical", "risk"]
    
    for topic in topics:
        print(f"\n💡 Lời khuyên về: {topic}")
        print("-" * 40)
        
        try:
            response = fingpt.get_investment_tips(topic)
            print(f"Độ tin cậy: {response.confidence:.1%}")
            print(f"Nguồn: {response.source}")
            print(f"Nội dung:\n{response.answer}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo FinGPT Model hoàn thành!")
    print("=" * 50)
    
    print("\n💡 **Hướng dẫn sử dụng:**")
    print("1. Cài đặt Ollama: https://ollama.ai")
    print("2. Fine-tune model: python scripts/finetune_fingpt.py")
    print("3. Sử dụng trong Telegram Bot:")
    print("   - Thay thế GPTAssistant bằng FinGPTModel")
    print("   - Model sẽ trả lời thông minh hơn về tài chính VN")

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
        return False

def main():
    """Main function"""
    print("🤖 FinGPT Model Demo")
    print("=" * 40)
    
    # Test Ollama connection first
    if not test_ollama_connection():
        print("\n⚠️ Ollama chưa sẵn sàng, chạy demo với fallback mode...")
    
    # Run demo
    demo_fingpt_model()

if __name__ == "__main__":
    main() 