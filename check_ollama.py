#!/usr/bin/env python3
"""
Check Ollama Status and Test Llama2 Model
Script để kiểm tra Ollama có hoạt động không và test model Llama2
"""

import subprocess
import sys
import time

def check_ollama_installed():
    """Kiểm tra Ollama đã được cài đặt chưa"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama đã được cài đặt: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama không hoạt động")
            return False
    except FileNotFoundError:
        print("❌ Ollama chưa được cài đặt")
        print("💡 Hướng dẫn cài đặt: https://ollama.ai/download")
        return False

def check_ollama_running():
    """Kiểm tra Ollama service có đang chạy không"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama service đang chạy")
            return True
        else:
            print("❌ Ollama service không chạy")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra Ollama: {e}")
        return False

def check_llama2_model():
    """Kiểm tra model Llama2 có sẵn không"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            if "llama2" in result.stdout.lower():
                print("✅ Model Llama2 đã có sẵn")
                return True
            else:
                print("⚠️ Model Llama2 chưa có, đang tải...")
                return download_llama2_model()
        else:
            print("❌ Không thể kiểm tra models")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra models: {e}")
        return False

def download_llama2_model():
    """Tải model Llama2"""
    try:
        print("📥 Đang tải model llama2:7b...")
        result = subprocess.run(["ollama", "pull", "llama2:7b"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Đã tải thành công model llama2:7b")
            return True
        else:
            print(f"❌ Lỗi khi tải model: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi tải model: {e}")
        return False

def test_llama2_model():
    """Test model Llama2 với câu hỏi đơn giản"""
    try:
        print("🧪 Đang test model Llama2...")
        test_question = "Xin chào, bạn có thể giúp tôi không?"
        
        cmd = ["ollama", "run", "llama2:7b", f"<s>[INST] {test_question} [/INST]"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Model Llama2 hoạt động tốt!")
            print(f"📝 Test response: {result.stdout.strip()[:100]}...")
            return True
        else:
            print(f"❌ Model Llama2 không trả lời: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Timeout khi test model (có thể model đang khởi động)")
        return False
    except Exception as e:
        print(f"❌ Lỗi khi test model: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Kiểm tra Ollama và Llama2 Model")
    print("=" * 50)
    
    # Check installation
    if not check_ollama_installed():
        sys.exit(1)
    
    # Check service
    if not check_ollama_running():
        print("💡 Hãy khởi động Ollama service trước")
        sys.exit(1)
    
    # Check model
    if not check_llama2_model():
        print("💡 Hãy cài đặt model Llama2 trước")
        sys.exit(1)
    
    # Test model
    if not test_llama2_model():
        print("💡 Model Llama2 có vấn đề, hãy kiểm tra lại")
        sys.exit(1)
    
    print("\n🎉 Tất cả đều hoạt động tốt!")
    print("✅ Bot có thể sử dụng Llama2 model")
    print("\n💡 Để chạy bot:")
    print("   source venv/bin/activate")
    print("   python run_telegram_bot.py")

if __name__ == "__main__":
    main() 