"""
Demo Claude Assistant
Test Claude AI integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

# Load environment variables
load_dotenv('.env')

from src.ai.claude_assistant import ClaudeAssistant

def test_claude_assistant():
    """Test Claude Assistant functionality"""
    print("🤖 Testing Claude Assistant...")
    
    try:
        # Initialize Claude Assistant
        claude = ClaudeAssistant()
        print("✅ Claude Assistant initialized successfully")
        
        # Test questions
        test_questions = [
            "RSI là gì và cách sử dụng?",
            "Làm thế nào để quản lý rủi ro khi đầu tư?",
            "Phân tích xu hướng thị trường Việt Nam hiện tại?",
            "MACD là gì?",
            "Sharpe Ratio có ý nghĩa gì trong đầu tư?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{'='*50}")
            print(f"Test {i}: {question}")
            print('='*50)
            
            try:
                # Get answer
                analysis = claude.analyze_question(question)
                response = claude.format_response(analysis)
                
                print(f"✅ Success!")
                print(f"Source: {analysis.get('source', 'unknown')}")
                print(f"Confidence: {analysis.get('confidence', 0):.1%}")
                if analysis.get('tokens_used'):
                    print(f"Tokens used: {analysis.get('tokens_used')}")
                
                print("\n📝 Answer:")
                print(response)
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Test investment tips
        print(f"\n{'='*50}")
        print("Test Investment Tips")
        print('='*50)
        
        topics = ["general", "beginner", "technical", "risk"]
        for topic in topics:
            tips = claude.get_investment_tips(topic)
            print(f"\n💡 Tips for {topic}:")
            for tip in tips:
                print(f"• {tip}")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize Claude Assistant: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure ANTHROPIC_API_KEY is set in config.env")
        print("2. Check your internet connection")
        print("3. Verify your API key is valid")

if __name__ == "__main__":
    test_claude_assistant() 