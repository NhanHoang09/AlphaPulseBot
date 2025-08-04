# 🤖 FinGPT Telegram Bot - Hướng dẫn sử dụng

## 📱 Tạo Bot Telegram

### Bước 1: Tạo bot với BotFather
1. Mở Telegram và tìm **@BotFather**
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (ví dụ: "FinGPT Financial Bot")
4. Đặt username cho bot (ví dụ: "fingpt_financial_bot")
5. BotFather sẽ trả về **token** - hãy lưu lại!

### Bước 2: Cấu hình token
1. Tạo file `.env` trong thư mục gốc
2. Thêm dòng sau:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```
3. Thay `your_bot_token_here` bằng token thật từ BotFather

## 🚀 Chạy Bot

### Cách 1: Chạy trực tiếp
```bash
python run_telegram_bot.py
```

### Cách 2: Chạy từ module
```bash
python src/bot/telegram_bot.py
```

## 📋 Các lệnh có sẵn

### 🎯 Lệnh cơ bản
- `/start` - Khởi động bot và xem menu
- `/help` - Xem hướng dẫn sử dụng

### 📈 Phân tích cổ phiếu
- `/stock <symbol>` - Phân tích cổ phiếu (tự động nhận diện thị trường)
- `/vn <symbol>` - Phân tích cổ phiếu Việt Nam
- `/us <symbol>` - Phân tích cổ phiếu Mỹ

**Ví dụ:**
```
/stock VNM
/stock AAPL
/vn TCB
/us MSFT
```

### 📊 Tối ưu hóa Portfolio
- `/portfolio <symbols>` - Tối ưu hóa danh mục đầu tư

**Ví dụ:**
```
/portfolio VNM,TCB,HPG
/portfolio AAPL,MSFT,GOOGL
```

### ⚠️ Phân tích rủi ro
- `/risk <symbol>` - Phân tích rủi ro cổ phiếu

**Ví dụ:**
```
/risk VNM
/risk AAPL
```

## 📊 Cổ phiếu được hỗ trợ

### 🇻🇳 Thị trường Việt Nam
- **VNM** - Vinamilk
- **TCB** - Techcombank
- **HPG** - Hòa Phát
- **FPT** - FPT
- **VIC** - Vingroup
- **VHM** - Vinhomes
- **VRE** - Vincom Retail
- **MWG** - Mobile World

### 🇺🇸 Thị trường Mỹ
- **AAPL** - Apple
- **MSFT** - Microsoft
- **GOOGL** - Google
- **AMZN** - Amazon
- **TSLA** - Tesla
- **META** - Meta (Facebook)
- **NVDA** - NVIDIA
- **NFLX** - Netflix

## 📈 Tính năng phân tích

### 🎯 Tín hiệu giao dịch
- **RSI** - Relative Strength Index
- **MACD** - Moving Average Convergence Divergence
- **Bollinger Bands** - Dải Bollinger
- **Moving Averages** - Đường trung bình động

### ⚠️ Chỉ số rủi ro
- **Sharpe Ratio** - Tỷ lệ Sharpe
- **Sortino Ratio** - Tỷ lệ Sortino
- **Max Drawdown** - Mức sụt giảm tối đa
- **VaR (95%)** - Value at Risk
- **CVaR (95%)** - Conditional Value at Risk
- **Volatility** - Độ biến động

### 📊 Portfolio Optimization
- **Expected Return** - Lợi nhuận kỳ vọng
- **Portfolio Volatility** - Độ biến động portfolio
- **Optimal Weights** - Trọng số tối ưu

## 🔧 Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Tạo file .env
```bash
cp config.env.example .env
# Chỉnh sửa file .env với token thật
```

### 3. Chạy bot
```bash
python run_telegram_bot.py
```

### 4. Sử dụng bot
1. Tìm bot của bạn trên Telegram
2. Gửi `/start`
3. Sử dụng các lệnh để phân tích

## 🎨 Giao diện bot

Bot có giao diện thân thiện với:
- ✅ Emoji và formatting đẹp
- 📊 Bảng thống kê rõ ràng
- 🎯 Tín hiệu giao dịch trực quan
- ⚠️ Cảnh báo rủi ro
- 📱 Responsive design

## 🔒 Bảo mật

- Token bot được lưu trong file `.env`
- Không chia sẻ token với người khác
- Bot chỉ phản hồi với người dùng được phép

## 🆘 Xử lý lỗi

### Lỗi thường gặp:
1. **"Token không hợp lệ"** - Kiểm tra lại token trong file .env
2. **"Không tìm thấy dữ liệu"** - Kiểm tra mã cổ phiếu
3. **"Lỗi kết nối"** - Kiểm tra internet

### Liên hệ hỗ trợ:
- Tạo issue trên GitHub
- Gửi email: nhanht2@rikkeisoft.com

## 🚀 Tính năng nâng cao

### 🤖 AI Prediction
- Dự báo giá với LSTM
- Ensemble models
- Confidence scoring

### 📊 Real-time Data
- Dữ liệu real-time từ Yahoo Finance
- Cập nhật tự động
- Historical data analysis

### ⚡ Performance
- Phản hồi nhanh
- Xử lý đa luồng
- Cache optimization

---

**🎉 Chúc bạn sử dụng FinGPT Telegram Bot hiệu quả!** 