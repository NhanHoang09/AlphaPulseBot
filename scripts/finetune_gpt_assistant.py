#!/usr/bin/env python3
"""
GPT Assistant Fine-tuning Script
Fine-tune Llama2 model for GPT Assistant with financial knowledge
"""

import json
import subprocess
import os
import sys
from pathlib import Path

class GPTAssistantFineTuner:
    """Fine-tune GPT Assistant model using Ollama"""
    
    def __init__(self, base_model: str = "llama2:7b", output_model: str = "gpt_assistant:latest"):
        self.base_model = base_model
        self.output_model = output_model
        self.dataset_path = "data/gpt_assistant_dataset.json"
        
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
    
    def create_gpt_assistant_dataset(self):
        """Create dataset for GPT Assistant"""
        dataset = {
            "training_data": [
                {
                    "instruction": "Giải thích RSI là gì?",
                    "input": "",
                    "output": "RSI (Relative Strength Index) là chỉ số sức mạnh tương đối, đo lường tốc độ và mức độ thay đổi giá. RSI > 70 cho thấy cổ phiếu có thể bị quá mua (overbought), RSI < 30 cho thấy có thể bị quá bán (oversold). Công thức: RSI = 100 - (100 / (1 + RS)), RS = Average Gain / Average Loss. RSI thường được sử dụng để xác định điểm vào lệnh khi cổ phiếu bị oversold (RSI < 30) hoặc thoát lệnh khi overbought (RSI > 70)."
                },
                {
                    "instruction": "MACD hoạt động như thế nào?",
                    "input": "",
                    "output": "MACD (Moving Average Convergence Divergence) so sánh hai đường trung bình động để xác định momentum. Khi MACD vượt lên trên đường Signal, đó là tín hiệu mua. Khi MACD xuống dưới Signal, đó là tín hiệu bán. Công thức: MACD = EMA(12) - EMA(26), Signal = EMA(9) của MACD. MACD được sử dụng để xác định xu hướng và momentum. Tín hiệu mua khi MACD vượt lên trên Signal, tín hiệu bán khi MACD xuống dưới Signal."
                },
                {
                    "instruction": "Bollinger Bands dùng để làm gì?",
                    "input": "",
                    "output": "Bollinger Bands đo lường biến động giá. Dải băng thu hẹp cho thấy biến động thấp, dải băng mở rộng cho thấy biến động cao. Giá chạm dải trên có thể báo hiệu overbought, chạm dải dưới có thể báo hiệu oversold. Công thức: Upper = SMA(20) + 2*StdDev, Lower = SMA(20) - 2*StdDev. Bollinger Bands giúp xác định biến động giá và điểm vào lệnh. Giá chạm dải dưới có thể là cơ hội mua, chạm dải trên có thể là cơ hội bán."
                },
                {
                    "instruction": "Sharpe Ratio quan trọng như thế nào?",
                    "input": "",
                    "output": "Sharpe Ratio đo lường lợi nhuận so với rủi ro. Sharpe > 1 là tốt, > 2 là rất tốt, < 0 là kém. Chỉ số này giúp so sánh hiệu quả đầu tư giữa các tài sản khác nhau. Sharpe Ratio cao hơn có nghĩa là nhà đầu tư nhận được lợi nhuận tốt hơn so với rủi ro phải chịu."
                },
                {
                    "instruction": "Làm thế nào để quản lý rủi ro?",
                    "input": "",
                    "output": "Để quản lý rủi ro hiệu quả: 1) Luôn đa dạng hóa portfolio để giảm rủi ro, 2) Không đầu tư quá 5-10% vào một cổ phiếu, 3) Sử dụng stop loss để bảo vệ vốn, 4) Tính toán risk/reward ratio trước khi vào lệnh, 5) Theo dõi các chỉ số rủi ro như VaR, Max Drawdown, 6) Có kế hoạch thoát lệnh rõ ràng, 7) Không để cảm xúc chi phối quyết định."
                },
                {
                    "instruction": "Có nên timing thị trường không?",
                    "input": "",
                    "output": "Timing thị trường rất khó và rủi ro cao. Thay vào đó, nên sử dụng Dollar Cost Averaging (đầu tư định kỳ) và tập trung vào phân tích cơ bản dài hạn. Timing thị trường đòi hỏi phải dự đoán chính xác cả điểm vào và điểm ra, điều này gần như không thể thực hiện được một cách nhất quán."
                },
                {
                    "instruction": "Làm thế nào để xây dựng portfolio?",
                    "input": "",
                    "output": "Xây dựng portfolio cần: 1) Xác định mục tiêu và khẩu vị rủi ro, 2) Đa dạng hóa theo ngành và thị trường, 3) Cân bằng giữa cổ phiếu tăng trưởng và giá trị, 4) Định kỳ rebalance. Portfolio nên bao gồm các loại tài sản khác nhau để giảm rủi ro và tăng cơ hội lợi nhuận."
                },
                {
                    "instruction": "Phân tích cơ bản là gì?",
                    "input": "",
                    "output": "Phân tích cơ bản là phương pháp đánh giá giá trị thực của cổ phiếu dựa trên các yếu tố tài chính và kinh tế. Bao gồm: 1) Phân tích báo cáo tài chính (P/E, P/B, ROE, ROA), 2) Đánh giá ngành nghề và vị thế cạnh tranh, 3) Phân tích môi trường kinh tế vĩ mô, 4) Xem xét quản trị và chiến lược công ty. Mục tiêu là xác định cổ phiếu bị định giá thấp so với giá trị thực."
                },
                {
                    "instruction": "Phân tích kỹ thuật là gì?",
                    "input": "",
                    "output": "Phân tích kỹ thuật là phương pháp dự đoán xu hướng giá dựa trên dữ liệu lịch sử giá và khối lượng. Bao gồm: 1) Phân tích biểu đồ giá (chart patterns), 2) Sử dụng các chỉ báo kỹ thuật (RSI, MACD, Bollinger Bands), 3) Phân tích khối lượng giao dịch, 4) Xác định support và resistance levels. Giả định cơ bản là giá phản ánh tất cả thông tin và có xu hướng lặp lại."
                },
                {
                    "instruction": "Đầu tư giá trị là gì?",
                    "input": "",
                    "output": "Đầu tư giá trị là chiến lược mua cổ phiếu bị định giá thấp so với giá trị thực. Nhà đầu tư giá trị tìm kiếm: 1) Cổ phiếu có P/E, P/B thấp, 2) Công ty có tài sản mạnh và ít nợ, 3) Cổ phiếu bị thị trường bỏ qua, 4) Công ty có lợi nhuận ổn định. Chiến lược này đòi hỏi kiên nhẫn và có thể mất thời gian để thị trường nhận ra giá trị thực."
                }
            ]
        }
        
        # Save dataset
        os.makedirs("data", exist_ok=True)
        with open(self.dataset_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã tạo dataset tại: {self.dataset_path}")
        return dataset
    
    def create_modelfile(self) -> str:
        """Create Modelfile for fine-tuning"""
        system_prompt = """Bạn là AI chuyên gia tài chính Việt Nam, chuyên về:
- Phân tích kỹ thuật (RSI, MACD, Bollinger Bands, Moving Averages)
- Quản lý rủi ro và đầu tư
- Thị trường chứng khoán Việt Nam
- Chiến lược đầu tư và xây dựng portfolio

Hãy trả lời bằng tiếng Việt, chính xác và hữu ích cho nhà đầu tư Việt Nam."""
        
        modelfile_content = f"""FROM {self.base_model}

# Set system prompt for GPT Assistant
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
            print("Tạo dataset mới...")
            self.create_gpt_assistant_dataset()
            
            # Load again
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data.get('training_data', []):
                instruction = item.get('instruction', '')
                output = item.get('output', '')
                modelfile_content += f'PROMPT "{instruction}"\nRESPONSE "{output}"\n\n'
        
        return modelfile_content
    
    def save_modelfile(self, content: str) -> str:
        """Save Modelfile to disk"""
        modelfile_path = "Modelfile.gpt_assistant"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Đã tạo Modelfile tại: {modelfile_path}")
        return modelfile_path
    
    def fine_tune_model(self) -> bool:
        """Fine-tune the model using Ollama"""
        print(f"\n🚀 Bắt đầu fine-tune model {self.output_model}...")
        
        try:
            # Create model using Modelfile
            cmd = ["ollama", "create", self.output_model, "-f", "Modelfile.gpt_assistant"]
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
            "MACD hoạt động như thế nào?",
            "Làm thế nào để quản lý rủi ro?",
            "Có nên timing thị trường không?"
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
        print("🤖 GPT Assistant Fine-tuning Process")
        print("=" * 50)
        
        # Step 1: Check Ollama
        if not self.check_ollama_installation():
            return False
        
        # Step 2: Check base model
        if not self.check_base_model():
            return False
        
        # Step 3: Create dataset
        print("\n📝 Tạo dataset...")
        self.create_gpt_assistant_dataset()
        
        # Step 4: Create Modelfile
        print("\n📝 Tạo Modelfile...")
        modelfile_content = self.create_modelfile()
        self.save_modelfile(modelfile_content)
        
        # Step 5: Fine-tune
        if not self.fine_tune_model():
            return False
        
        # Step 6: Test
        self.test_model()
        
        print(f"\n🎉 Hoàn thành! Model GPT Assistant: {self.output_model}")
        print("\n💡 Sử dụng model:")
        print(f"   ollama run {self.output_model} 'Câu hỏi của bạn'")
        print("\n🔧 Cập nhật GPT Assistant:")
        print("   assistant = GPTAssistant(model_name='gpt_assistant:latest')")
        
        return True

def main():
    """Main function"""
    print("🤖 GPT Assistant Model Fine-tuning")
    print("=" * 40)
    
    # Configuration
    base_model = "llama2:7b"  # Base model
    output_model = "gpt_assistant:latest"  # Output model name
    
    # Create fine-tuner
    fine_tuner = GPTAssistantFineTuner(base_model, output_model)
    
    # Run fine-tuning
    success = fine_tuner.run_fine_tuning()
    
    if success:
        print("\n✅ Fine-tuning thành công!")
        print(f"Model GPT Assistant: {output_model}")
    else:
        print("\n❌ Fine-tuning thất bại!")
        sys.exit(1)

if __name__ == "__main__":
    main() 