"""
Demo GPT Assistant
Demo AI trợ lý thông minh để hỏi đáp và giải thích kỹ thuật đầu tư
"""

import sys
import os
sys.path.append('src')

from src.ai.gpt_assistant import GPTAssistant

def demo_gpt_assistant():
    """Demo GPT Assistant"""
    print("🤖 GPT Assistant Demo")
    print("="*60)
    
    # Initialize GPT Assistant
    assistant = GPTAssistant()
    
    # Test questions
    test_questions = [
        "RSI là gì?",
        "MACD hoạt động như thế nào?",
        "Bollinger Bands dùng để làm gì?",
        "Sharpe Ratio quan trọng như thế nào?",
        "Làm thế nào để quản lý rủi ro?",
        "Có nên timing thị trường không?",
        "Làm thế nào để xây dựng portfolio?",
        "Moving Averages là gì?",
        "Value at Risk là gì?",
        "Chiến lược đầu tư nào tốt nhất?"
    ]
    
    # Test indicators
    test_indicators = [
        "RSI",
        "MACD", 
        "Bollinger",
        "Moving Averages"
    ]
    
    # Test tips
    test_topics = [
        "general",
        "technical", 
        "risk"
    ]
    
    print("\n🔍 **Demo: Hỏi đáp AI**")
    print("="*40)
    
    for i, question in enumerate(test_questions[:5], 1):
        print(f"\n{i}. Câu hỏi: {question}")
        print("-" * 30)
        
        try:
            analysis = assistant.analyze_question(question)
            response = assistant.format_response(analysis)
            print(f"Độ tin cậy: {analysis.get('confidence', 0):.1%}")
            print(f"Loại: {analysis.get('type', 'unknown')}")
            print(f"Trả lời: {response}")
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    print("\n📚 **Demo: Giải thích chỉ báo**")
    print("="*40)
    
    for indicator in test_indicators:
        print(f"\n📊 Giải thích: {indicator}")
        print("-" * 30)
        
        try:
            explanation = assistant.explain_indicator(indicator)
            if 'error' not in explanation:
                print(f"Tên: {explanation['name']}")
                print(f"Mô tả: {explanation['description']}")
                print(f"Cách hiểu: {explanation['interpretation']}")
                print(f"Công thức: {explanation['calculation']}")
                print(f"Cách sử dụng: {explanation['usage']}")
            else:
                print(f"❌ {explanation['error']}")
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    print("\n💡 **Demo: Lời khuyên đầu tư**")
    print("="*40)
    
    for topic in test_topics:
        print(f"\n💡 Lời khuyên về: {topic}")
        print("-" * 30)
        
        try:
            tips = assistant.get_investment_tips(topic)
            for i, tip in enumerate(tips, 1):
                print(f"{i}. {tip}")
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🎉 Demo GPT Assistant hoàn thành!")
    print("="*60)
    print("\nĐể sử dụng GPT Assistant trong Telegram Bot:")
    print("   /ask RSI là gì? - Hỏi về RSI")
    print("   /explain MACD - Giải thích MACD")
    print("   /tips risk - Lời khuyên quản lý rủi ro")

if __name__ == "__main__":
    demo_gpt_assistant() 