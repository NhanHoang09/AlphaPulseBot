# 🤖 FinGPT Model - Hướng dẫn sử dụng

## **📋 Tổng quan**

**FinGPT Model** là một AI model tùy chỉnh được fine-tune cho phân tích tài chính Việt Nam, thay thế GPT Assistant hiện tại với khả năng thông minh hơn và chuyên biệt hơn.

## **🚀 Cài đặt và Setup**

### **1. Cài đặt Ollama**

```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Hoặc download từ: https://ollama.ai
```

### **2. Tải Base Model**

```bash
# Tải Llama2:7b (khuyến nghị)
ollama pull llama2:7b

# Hoặc các model khác
ollama pull mistral:7b
ollama pull phi:2
```

### **3. Fine-tune FinGPT Model**

```bash
# Chạy script fine-tuning
python scripts/finetune_fingpt.py
```

## **🤖 Sử dụng FinGPT Model**

### **1. Test Model**

```bash
# Test cơ bản
ollama run fingpt:latest "RSI là gì?"

# Test với context
ollama run fingpt:latest "VNM có RSI = 75, có nên bán không?"
```

### **2. Demo Python**

```bash
# Chạy demo
python demo_fingpt_model.py
```

### **3. Tích hợp vào Telegram Bot**

Model đã được tích hợp sẵn vào Telegram Bot. Sử dụng các lệnh:

- `/ask <câu hỏi>` - Hỏi đáp với FinGPT
- `/explain <chỉ báo>` - Giải thích chỉ báo
- `/tips <chủ đề>` - Lời khuyên đầu tư

## **📊 Tính năng FinGPT Model**

### **✅ Ưu điểm:**

- **Chuyên biệt:** Tối ưu cho tài chính Việt Nam
- **Tiếng Việt:** Hiểu và trả lời tiếng Việt tốt
- **Local:** Chạy trên máy, không cần internet
- **Fine-tunable:** Có thể training thêm
- **Fast:** Phản hồi nhanh
- **Free:** Hoàn toàn miễn phí

### **🔧 Tính năng:**

1. **Hỏi đáp tài chính:** RSI, MACD, Bollinger Bands
2. **Phân tích thị trường VN:** VNM, TCB, HPG, VCB
3. **Quản lý rủi ro:** VaR, Sharpe Ratio, Max Drawdown
4. **Lời khuyên đầu tư:** Chiến lược, timing, portfolio
5. **Giải thích kỹ thuật:** Công thức, cách sử dụng

## **📈 So sánh với GPT Assistant cũ**

| Tính năng       | GPT Assistant (cũ) | FinGPT Model (mới) |
| --------------- | ------------------ | ------------------ |
| **Dữ liệu**     | Hard-coded         | AI thông minh      |
| **Tiếng Việt**  | ⭐⭐⭐             | ⭐⭐⭐⭐⭐         |
| **Context**     | ⭐⭐               | ⭐⭐⭐⭐⭐         |
| **Tùy chỉnh**   | ❌                 | ⭐⭐⭐⭐⭐         |
| **Local**       | ❌                 | ⭐⭐⭐⭐⭐         |
| **Chi phí**     | Free               | Free               |
| **Performance** | ⭐⭐⭐             | ⭐⭐⭐⭐⭐         |

## **🎯 Ví dụ sử dụng**

### **Câu hỏi đơn giản:**

```
User: "RSI là gì?"
FinGPT: "RSI (Relative Strength Index) là chỉ số sức mạnh tương đối..."
```

### **Câu hỏi phức tạp:**

```
User: "VNM có RSI = 75, MACD đang giảm, có nên bán không?"
FinGPT: "Dựa trên các chỉ báo của VNM:
- RSI 75: Đang ở vùng overbought
- MACD giảm: Momentum yếu
- Khuyến nghị: Chốt lời một phần..."
```

### **Phân tích thị trường:**

```
User: "Thị trường Việt Nam có đặc điểm gì?"
FinGPT: "Thị trường VN có những đặc điểm:
1) Quy mô nhỏ, biến động cao
2) Thanh khoản tập trung vào blue-chip
3) Chịu ảnh hưởng mạnh từ chính sách..."
```

## **🔧 Fine-tuning nâng cao**

### **1. Thêm dữ liệu training**

Chỉnh sửa file `data/fingpt_dataset.json`:

```json
{
  "instruction": "Câu hỏi mới",
  "input": "Context bổ sung",
  "output": "Câu trả lời mong muốn"
}
```

### **2. Custom Model**

```bash
# Tạo model tùy chỉnh
ollama create myfingpt:latest -f Modelfile

# Sử dụng model
ollama run myfingpt:latest "Câu hỏi"
```

### **3. Training với dữ liệu thực**

- Thu thập dữ liệu từ các báo cáo tài chính
- Tích hợp tin tức thị trường
- Cập nhật kiến thức về ngành

## **⚠️ Troubleshooting**

### **Lỗi thường gặp:**

1. **"Ollama not found"**

   ```bash
   # Cài đặt lại Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **"Model not found"**

   ```bash
   # Tải model
   ollama pull llama2:7b
   ollama pull fingpt:latest
   ```

3. **"Connection timeout"**

   ```bash
   # Khởi động Ollama
   ollama serve
   ```

4. **"Memory insufficient"**
   - Giảm model size: `ollama pull phi:2`
   - Tăng RAM hoặc sử dụng swap

## **📚 Tài liệu tham khảo**

- **Ollama Docs:** https://ollama.ai/docs
- **Llama2 Paper:** https://arxiv.org/abs/2307.09288
- **Fine-tuning Guide:** https://github.com/ollama/ollama
- **Vietnamese Finance:** Các báo cáo VNDIRECT, SSI

## **🎉 Kết luận**

FinGPT Model là bước tiến quan trọng trong việc tạo ra AI chuyên gia tài chính Việt Nam. Model này:

- ✅ **Thông minh hơn** GPT Assistant cũ
- ✅ **Chuyên biệt** cho thị trường VN
- ✅ **Có thể training** thêm
- ✅ **Hoàn toàn local** và miễn phí
- ✅ **Tích hợp dễ dàng** vào Telegram Bot

**Bắt đầu sử dụng ngay:** `python demo_fingpt_model.py`
