"""
Test Claude Command
Kiểm tra nhanh Claude command
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Add src to path
sys.path.append('src')

from src.ai.claude_assistant import ClaudeAssistant

def test_claude_command():
    """Test Claude command functionality"""
    print("🤖 Testing Claude Command...")
    
    try:
        # Initialize Claude Assistant
        claude = ClaudeAssistant()
        print("✅ Claude Assistant initialized successfully")
        
        # Test a simple question
        question = "RSI là gì?"
        print(f"\n📝 Testing question: {question}")
        
        # Get answer
        analysis = claude.analyze_question(question)
        response = claude.format_response(analysis)
        
        print(f"✅ Success!")
        print(f"Source: {analysis.get('source', 'unknown')}")
        print(f"Confidence: {analysis.get('confidence', 0):.1%}")
        
        print("\n📝 Answer:")
        print(response)
        
        # Test Claude command format
        print(f"\n🤖 Claude Command format:")
        print(f"/claude {question}")
        
        print("\n✅ Claude command is ready to use!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_claude_command() 