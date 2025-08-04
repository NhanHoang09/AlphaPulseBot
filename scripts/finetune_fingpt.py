#!/usr/bin/env python3
"""
FinGPT Fine-tuning Script
Fine-tune Llama2 model for Vietnamese financial analysis
"""

import json
import subprocess
import os
import sys
from pathlib import Path

class FinGPTFineTuner:
    """Fine-tune FinGPT model using Ollama"""
    
    def __init__(self, base_model: str = "llama2:7b", output_model: str = "fingpt:latest"):
        self.base_model = base_model
        self.output_model = output_model
        self.dataset_path = "data/fingpt_dataset.json"
        
    def check_ollama_installation(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Ollama đã được cài đặt: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("❌ Ollama chưa được cài đặt!")
        print("\n🔧 Hướng dẫn cài đặt Ollama:")
        print("1. Truy cập: https://ollama.ai")
        print("2. Download và cài đặt cho macOS")
        print("3. Hoặc chạy: curl -fsSL https://ollama.ai/install.sh | sh")
        return False
    
    def check_base_model(self) -> bool:
        """Check if base model is available"""
        try:
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and self.base_model in result.stdout:
                print(f"✅ Base model {self.base_model} đã có sẵn")
                return True
        except subprocess.TimeoutExpired:
            pass
        
        print(f"❌ Base model {self.base_model} chưa có!")
        print(f"\n🔧 Đang tải model {self.base_model}...")
        try:
            subprocess.run(["ollama", "pull", self.base_model], check=True)
            print(f"✅ Đã tải xong {self.base_model}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi tải model: {e}")
            return False
    
    def create_modelfile(self) -> str:
        """Create Modelfile for fine-tuning"""
        system_prompt = """Bạn là FinGPT - AI chuyên gia tài chính Việt Nam. 
Bạn có kiến thức sâu rộng về:
- Phân tích kỹ thuật (RSI, MACD, Bollinger Bands)
- Thị trường chứng khoán Việt Nam
- Quản lý rủi ro và đầu tư
- Các chỉ số tài chính và báo cáo

Hãy trả lời bằng tiếng Việt, chính xác và hữu ích cho nhà đầu tư Việt Nam."""
        
        modelfile_content = f"""FROM {self.base_model}

# Set system prompt for financial analysis
SYSTEM "{system_prompt}"

# Add training data
"""
        
        # Load training data
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data.get('training_data', []):
                instruction = item.get('instruction', '')
                output = item.get('output', '')
                modelfile_content += f'PROMPT "{instruction}"\nRESPONSE "{output}"\n\n'
                
        except FileNotFoundError:
            print(f"⚠️ Không tìm thấy dataset tại {self.dataset_path}")
            print("Sử dụng prompt cơ bản...")
        
        return modelfile_content
    
    def save_modelfile(self, content: str) -> str:
        """Save Modelfile to disk"""
        modelfile_path = "Modelfile"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Đã tạo Modelfile tại: {modelfile_path}")
        return modelfile_path
    
    def fine_tune_model(self) -> bool:
        """Fine-tune the model using Ollama"""
        print(f"\n🚀 Bắt đầu fine-tune model {self.output_model}...")
        
        try:
            # Create model using Modelfile
            cmd = ["ollama", "create", self.output_model, "-f", "Modelfile"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Fine-tune thành công! Model: {self.output_model}")
                return True
            else:
                print(f"❌ Lỗi fine-tune: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Fine-tune timeout (có thể mất nhiều thời gian)")
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def test_model(self) -> bool:
        """Test the fine-tuned model"""
        print(f"\n🧪 Test model {self.output_model}...")
        
        test_questions = [
            "RSI là gì?",
            "Có nên đầu tư vào VNM không?",
            "Thị trường Việt Nam có đặc điểm gì?"
        ]
        
        for question in test_questions:
            print(f"\n❓ Câu hỏi: {question}")
            try:
                cmd = ["ollama", "run", self.output_model, question]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"🤖 Trả lời: {result.stdout.strip()}")
                else:
                    print(f"❌ Lỗi: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print("⏰ Timeout")
            except Exception as e:
                print(f"❌ Lỗi: {e}")
    
    def run_fine_tuning(self):
        """Run complete fine-tuning process"""
        print("🤖 FinGPT Fine-tuning Process")
        print("=" * 50)
        
        # Step 1: Check Ollama
        if not self.check_ollama_installation():
            return False
        
        # Step 2: Check base model
        if not self.check_base_model():
            return False
        
        # Step 3: Create Modelfile
        print("\n📝 Tạo Modelfile...")
        modelfile_content = self.create_modelfile()
        self.save_modelfile(modelfile_content)
        
        # Step 4: Fine-tune
        if not self.fine_tune_model():
            return False
        
        # Step 5: Test
        self.test_model()
        
        print(f"\n🎉 Hoàn thành! Model FinGPT: {self.output_model}")
        print("\n💡 Sử dụng model:")
        print(f"   ollama run {self.output_model} 'Câu hỏi của bạn'")
        
        return True

def main():
    """Main function"""
    print("🤖 FinGPT Model Fine-tuning")
    print("=" * 40)
    
    # Configuration
    base_model = "llama2:7b"  # Base model
    output_model = "fingpt:latest"  # Output model name
    
    # Create fine-tuner
    fine_tuner = FinGPTFineTuner(base_model, output_model)
    
    # Run fine-tuning
    success = fine_tuner.run_fine_tuning()
    
    if success:
        print("\n✅ Fine-tuning thành công!")
        print(f"Model FinGPT: {output_model}")
    else:
        print("\n❌ Fine-tuning thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main() 