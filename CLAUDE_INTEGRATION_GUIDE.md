# Claude AI Integration Guide

## 🤖 Tích hợp Claude AI vào AlphaPulse Bot

### 📋 Tổng quan

Claude AI đã được tích hợp thành công vào AlphaPulse Bot, cung cấp khả năng hỏi đáp thông minh về tài chính và đầu tư sử dụng Claude 3.5 Sonnet API.

### 🚀 Tính năng mới

#### 1. Claude AI Assistant

- **Command**: `/claude <câu hỏi>`
- **Ví dụ**:
  - `/claude RSI là gì?`
  - `/claude Làm thế nào để quản lý rủi ro?`
  - `/claude Phân tích xu hướng thị trường VN?`

#### 2. Menu Claude AI

- Truy cập qua menu chính: "🤖 Claude AI"
- Hiển thị hướng dẫn sử dụng chi tiết
- Kiểm tra trạng thái kết nối API

#### 3. Fallback System

- Tự động chuyển sang knowledge base nếu API không khả dụng
- Đảm bảo bot luôn hoạt động ổn định

### 🔧 Cài đặt

#### 1. Đăng ký Anthropic API

1. Truy cập https://console.anthropic.com
2. Tạo tài khoản mới
3. Tạo API key
4. Copy API key

#### 2. Cấu hình Environment

Thêm vào file `config.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### 3. Cài đặt Dependencies

```bash
pip install anthropic>=0.7.0
```

### 🧪 Testing

#### 1. Test Claude Assistant

```bash
python demo_claude_assistant.py
```

#### 2. Test trong Bot

1. Khởi động bot: `python run_telegram_bot.py`
2. Gửi lệnh: `/claude RSI là gì?`
3. Kiểm tra response

### 📊 So sánh AI Models

| Tính năng        | GPT Assistant (Ollama) | Claude AI (API)   |
| ---------------- | ---------------------- | ----------------- |
| **Model**        | Local Ollama           | Claude 3.5 Sonnet |
| **Tốc độ**       | Nhanh (local)          | Trung bình (API)  |
| **Độ chính xác** | Tốt                    | Rất tốt           |
| **Chi phí**      | Miễn phí               | Có phí theo token |
| **Offline**      | ✅ Có                  | ❌ Không          |
| **Fallback**     | Knowledge base         | Knowledge base    |

### 🎯 Sử dụng

#### 1. Commands cơ bản

```bash
# Hỏi đáp tài chính
/claude RSI là gì?
/claude Làm thế nào để quản lý rủi ro?

# Giải thích chỉ báo
/explain MACD
/explain Bollinger

# Lời khuyên đầu tư
/tips general
/tips technical
/tips risk
```

#### 2. Menu Navigation

1. Gửi `/start` để mở menu chính
2. Chọn "🤖 Claude AI"
3. Xem hướng dẫn sử dụng
4. Sử dụng các lệnh được gợi ý

### 🔍 Troubleshooting

#### 1. Claude AI không khởi tạo được

**Lỗi**: "Claude AI Assistant chưa được khởi tạo"

**Giải pháp**:

- Kiểm tra `ANTHROPIC_API_KEY` trong `config.env`
- Đảm bảo API key hợp lệ
- Kiểm tra kết nối internet

#### 2. API Rate Limit

**Lỗi**: "Rate limit exceeded"

**Giải pháp**:

- Đợi một lúc rồi thử lại
- Nâng cấp plan API nếu cần
- Sử dụng fallback knowledge base

#### 3. Timeout

**Lỗi**: "Request timeout"

**Giải pháp**:

- Kiểm tra kết nối internet
- Thử lại sau vài giây
- Sử dụng câu hỏi ngắn gọn hơn

### 📈 Monitoring

#### 1. Logs

Bot sẽ log các thông tin:

- Khởi tạo Claude Assistant
- Số lượng tokens sử dụng
- Lỗi API (nếu có)
- Fallback usage

#### 2. Metrics

- Tỷ lệ thành công API calls
- Số lượng tokens tiêu thụ
- Thời gian response trung bình

### 🔒 Security

#### 1. API Key Protection

- Không commit API key vào git
- Sử dụng environment variables
- Rotate API key định kỳ

#### 2. Rate Limiting

- Bot có built-in rate limiting
- Fallback system để tránh downtime
- Error handling cho API failures

### 🚀 Tương lai

#### 1. Tính năng sắp tới

- [ ] Claude 3.5 Sonnet support
- [ ] Streaming responses
- [ ] Multi-language support
- [ ] Custom prompts per user

#### 2. Optimization

- [ ] Response caching
- [ ] Token usage optimization
- [ ] Better error handling
- [ ] Performance monitoring

### 📞 Support

Nếu gặp vấn đề:

1. Kiểm tra logs trong console
2. Chạy `demo_claude_assistant.py` để test
3. Kiểm tra API key và kết nối internet
4. Tạo issue trên GitHub nếu cần

---

**Lưu ý**: Claude AI sử dụng API có phí. Hãy theo dõi usage để tránh chi phí phát sinh ngoài ý muốn.
