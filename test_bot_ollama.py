"""
Test Bot Ollama Integration
Kiểm tra bot có thể gọi Ollama không
"""

import sys
import os
import subprocess

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_bot_ollama():
    """Test bot Ollama integration"""
    print("🤖 Testing Bot Ollama Integration...")
    
    # Test question
    question = "Làm thế nào để quản lý rủi ro?"
    
    try:
        print(f"📝 Testing question: {question}")
        print("🔄 Testing Ollama command directly...")
        
        # Test Ollama command directly (same as bot)
        cmd = ["ollama", "run", "gpt_assistant_v3:latest", question]
        print(f"Command: {' '.join(cmd[:3])}...")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        print(f"Return code: {result.returncode}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            answer = result.stdout.strip()
            print(f"✅ SUCCESS: Ollama response length: {len(answer)} characters")
            
            # Check if response contains Vietnamese
            vietnamese_chars = ['à', 'á', 'ạ', 'ả', 'ã', 'â', 'ầ', 'ấ', 'ậ', 'ẩ', 'ẫ', 'ă', 'ằ', 'ắ', 'ặ', 'ẳ', 'ẵ', 
                              'è', 'é', 'ẹ', 'ẻ', 'ẽ', 'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ', 'ì', 'í', 'ị', 'ỉ', 'ĩ', 
                              'ò', 'ó', 'ọ', 'ỏ', 'õ', 'ô', 'ồ', 'ố', 'ộ', 'ổ', 'ỗ', 'ơ', 'ờ', 'ớ', 'ợ', 'ở', 'ỡ', 
                              'ù', 'ú', 'ụ', 'ủ', 'ũ', 'ư', 'ừ', 'ứ', 'ự', 'ử', 'ữ', 'ỳ', 'ý', 'ỵ', 'ỷ', 'ỹ', 
                              'đ']
            
            has_vietnamese = any(char in answer.lower() for char in vietnamese_chars)
            print(f"🇻🇳 Contains Vietnamese: {'✅ YES' if has_vietnamese else '❌ NO'}")
            
            print("\n📝 Response preview:")
            print("="*50)
            print(answer[:200] + "..." if len(answer) > 200 else answer)
            print("="*50)
            
        else:
            print(f"❌ FAILED: Ollama returned error code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("❌ Ollama timeout")
    except FileNotFoundError:
        print("❌ Ollama not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_bot_ollama() 