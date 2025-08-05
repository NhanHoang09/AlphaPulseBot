"""
Test Mistral Vietnamese Response
Kiểm tra Mistral model có trả lời bằng tiếng Việt không
"""

import subprocess
import sys

def test_mistral_vietnamese():
    """Test Mistral Vietnamese response"""
    print("🤖 Testing Mistral Vietnamese Response...")
    
    # Test question
    question = "Làm thế nào để quản lý rủi ro?"
    
    try:
        print(f"📝 Testing question: {question}")
        print("🔄 Calling Mistral model...")
        
        # Call Mistral model
        cmd = ["ollama", "run", "gpt_assistant_v3:latest", question]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            answer = result.stdout.strip()
            print("✅ Mistral response received!")
            print(f"📊 Response length: {len(answer)} characters")
            
            # Check if response contains Vietnamese
            vietnamese_chars = ['à', 'á', 'ạ', 'ả', 'ã', 'â', 'ầ', 'ấ', 'ậ', 'ẩ', 'ẫ', 'ă', 'ằ', 'ắ', 'ặ', 'ẳ', 'ẵ', 
                              'è', 'é', 'ẹ', 'ẻ', 'ẽ', 'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ', 'ì', 'í', 'ị', 'ỉ', 'ĩ', 
                              'ò', 'ó', 'ọ', 'ỏ', 'õ', 'ô', 'ồ', 'ố', 'ộ', 'ổ', 'ỗ', 'ơ', 'ờ', 'ớ', 'ợ', 'ở', 'ỡ', 
                              'ù', 'ú', 'ụ', 'ủ', 'ũ', 'ư', 'ừ', 'ứ', 'ự', 'ử', 'ữ', 'ỳ', 'ý', 'ỵ', 'ỷ', 'ỹ', 
                              'đ']
            
            has_vietnamese = any(char in answer.lower() for char in vietnamese_chars)
            
            print(f"🇻🇳 Contains Vietnamese: {'✅ YES' if has_vietnamese else '❌ NO'}")
            
            if has_vietnamese:
                print("🎉 SUCCESS: Mistral is responding in Vietnamese!")
            else:
                print("⚠️ WARNING: Mistral is not responding in Vietnamese")
            
            print("\n📝 Full response:")
            print("="*50)
            print(answer)
            print("="*50)
            
        else:
            print(f"❌ Mistral failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Mistral timeout")
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mistral_vietnamese() 