#!/usr/bin/env python3
"""
Test GPT Assistant với Ollama
Kiểm tra GPT Assistant sử dụng Ollama thay vì data cứng
"""

import sys
import os
sys.path.append('src')

from src.ai.gpt_assistant import GPTAssistant

def test_gpt_assistant():
    """Test GPT Assistant với Ollama"""
    print("🧪 Test GPT Assistant với Ollama")
    print("=" * 50)
    
    # Initialize GPT Assistant
    assistant = GPTAssistant(model_name="gpt_assistant:latest")
    
    # Test questions
    test_questions = [
        "RSI là gì?",
        "MACD hoạt động như thế nào?",
        "Làm thế nào để quản lý rủi ro?",
        "Có nên đầu tư vào VNM không?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Câu hỏi: {question}")
        print("-" * 40)
        
        try:
            # Test analyze_question
            result = assistant.analyze_question(question)
            print(f"Loại: {result.get('type', 'unknown')}")
            print(f"Độ tin cậy: {result.get('confidence', 0):.1%}")
            print(f"Nguồn: {result.get('source', 'unknown')}")
            print(f"Model: {result.get('model_version', 'unknown')}")
            
            answer = result.get('answer', '')
            if answer:
                print(f"Trả lời: {answer[:200]}...")
            else:
                print("❌ Không có câu trả lời")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    # Test explain_indicator
    print(f"\n📊 Test explain_indicator:")
    print("-" * 40)
    
    try:
        result = assistant.explain_indicator("RSI")
        print(f"Loại: {result.get('type', 'unknown')}")
        print(f"Tên: {result.get('name', 'N/A')}")
        description = result.get('description', '')
        if description:
            print(f"Mô tả: {description[:200]}...")
        else:
            print("❌ Không có mô tả")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    
    # Test get_investment_tips
    print(f"\n💡 Test get_investment_tips:")
    print("-" * 40)
    
    try:
        tips = assistant.get_investment_tips("general")
        print(f"Số lượng tips: {len(tips)}")
        for i, tip in enumerate(tips, 1):
            print(f"{i}. {tip}")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    
    print(f"\n✅ Test hoàn thành!")

if __name__ == "__main__":
    test_gpt_assistant() 