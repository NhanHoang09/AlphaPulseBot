"""
Test Ollama Integration in Bot Environment
Kiểm tra tích hợp Ollama trong môi trường bot
"""

import sys
import os
import subprocess
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai.gpt_assistant import GPTAssistant

def test_ollama_integration():
    """Test Ollama integration"""
    print("🤖 Testing Ollama Integration...")
    
    # Test question
    question = "Làm thế nào để quản lý rủi ro?"
    
    try:
        print(f"📝 Testing question: {question}")
        print("🔄 Creating GPT Assistant...")
        
        # Create GPT Assistant
        assistant = GPTAssistant(model_name="gpt_assistant_v3:latest")
        
        print("🔄 Calling analyze_question...")
        
        # Test analyze_question
        result = assistant.analyze_question(question)
        
        print(f"✅ Result type: {result['type']}")
        print(f"📊 Confidence: {result['confidence']}")
        print(f"🤖 Source: {result['source']}")
        print(f"📝 Model version: {result['model_version']}")
        
        if result['type'] == 'ollama':
            print("🎉 SUCCESS: Ollama is working!")
            print(f"📊 Response length: {len(result['answer'])} characters")
            
            # Check if response contains Vietnamese
            vietnamese_chars = ['à', 'á', 'ạ', 'ả', 'ã', 'â', 'ầ', 'ấ', 'ậ', 'ẩ', 'ẫ', 'ă', 'ằ', 'ắ', 'ặ', 'ẳ', 'ẵ', 
                              'è', 'é', 'ẹ', 'ẻ', 'ẽ', 'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ', 'ì', 'í', 'ị', 'ỉ', 'ĩ', 
                              'ò', 'ó', 'ọ', 'ỏ', 'õ', 'ô', 'ồ', 'ố', 'ộ', 'ổ', 'ỗ', 'ơ', 'ờ', 'ớ', 'ợ', 'ở', 'ỡ', 
                              'ù', 'ú', 'ụ', 'ủ', 'ũ', 'ư', 'ừ', 'ứ', 'ự', 'ử', 'ữ', 'ỳ', 'ý', 'ỵ', 'ỷ', 'ỹ', 
                              'đ']
            
            has_vietnamese = any(char in result['answer'].lower() for char in vietnamese_chars)
            print(f"🇻🇳 Contains Vietnamese: {'✅ YES' if has_vietnamese else '❌ NO'}")
            
        elif result['type'] == 'fallback':
            print("⚠️ WARNING: Using fallback response")
            print("🔍 This means Ollama is not working properly")
            
        print("\n📝 Full response:")
        print("="*50)
        print(result['answer'])
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama_integration() 