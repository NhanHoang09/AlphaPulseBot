# AlphaPulseBot - AI Trading & Investment Advisor

🤖 **AlphaPulseBot** là một bot AI thông minh phân tích và dự báo xu hướng tài chính, tích hợp Telegram Bot để cung cấp thông tin đầu tư real-time.

## 🌟 Tính năng chính

### 📊 Phân tích kỹ thuật nâng cao

- **Chỉ báo kỹ thuật**: RSI, MACD, Bollinger Bands, Stochastic, ATR
- **Mô hình giá**: Pattern recognition, Support/Resistance levels
- **Volume analysis**: Volume profile, OBV, VWAP
- **Trend analysis**: Moving averages, Ichimoku, Fibonacci retracements

### 🤖 AI/ML Dự báo xu hướng

- **Machine Learning Models**: LSTM, Random Forest, SVM, XGBoost
- **Time Series Forecasting**: Prophet, ARIMA, SARIMA
- **Sentiment Analysis**: News sentiment từ các nguồn tin tài chính
- **Risk Assessment**: VaR, Sharpe ratio, Maximum drawdown

### 📱 Telegram Bot Integration

- **Real-time alerts**: Thông báo tức thì khi có tín hiệu giao dịch
- **Interactive commands**: Phân tích cổ phiếu, portfolio, rủi ro
- **Portfolio tracking**: Theo dõi danh mục đầu tư
- **Custom alerts**: Cài đặt cảnh báo theo ý muốn

### 🎯 Quản lý rủi ro thông minh

- **Portfolio Optimization**: Modern Portfolio Theory
- **Risk Metrics**: VaR, CVaR, Sharpe ratio, Sortino ratio
- **Stop-loss recommendations**: Tự động đề xuất stop-loss
- **Diversification analysis**: Phân tích đa dạng hóa

### 📈 Giao diện Dashboard

- **Streamlit Dashboard**: Giao diện web trực quan
- **Real-time charts**: Biểu đồ tương tác với Plotly
- **Performance tracking**: Theo dõi hiệu suất đầu tư
- **Backtesting**: Kiểm tra chiến lược giao dịch

## 🚀 Cài đặt nhanh

### Yêu cầu hệ thống

- Python 3.8+
- Git
- 4GB RAM (khuyến nghị)

### Bước 1: Clone repository

```bash
git clone <repository-url>
cd AlphaPulseBot
```

### Bước 2: Tạo virtual environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Trên macOS/Linux:
source venv/bin/activate
# Trên Windows:
venv\Scripts\activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình môi trường

```bash
# Copy file cấu hình mẫu
cp config.env.example .env

# Chỉnh sửa file .env với API keys của bạn
nano .env
```

## ⚙️ Cấu hình API Keys

### Bắt buộc

- **Alpha Vantage API**: Lấy dữ liệu thị trường tài chính
  - Đăng ký tại: https://www.alphavantage.co/
  - Free tier: 500 requests/day

### Tùy chọn

- **News API**: Phân tích sentiment từ tin tức
  - Đăng ký tại: https://newsapi.org/
- **Telegram Bot Token**: Để sử dụng bot Telegram
  - Tạo bot tại: @BotFather trên Telegram

### Ví dụ file .env

```env
# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
NEWS_API_KEY=your_news_api_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_BOT_USERNAME=your_bot_username_here

# Trading Configuration
DEFAULT_TIMEFRAME=1d
DEFAULT_PERIOD=1y
RISK_TOLERANCE=medium
```

## 🎮 Cách sử dụng

### 1. Chạy Telegram Bot

```bash
python run_telegram_bot.py
```

**Các lệnh Telegram Bot:**

- `/start` - Bắt đầu bot
- `/stock VNM` - Phân tích cổ phiếu VNM
- `/stock AAPL` - Phân tích cổ phiếu Apple
- `/portfolio VNM,TCB,HPG` - Tối ưu portfolio
- `/risk VNM` - Phân tích rủi ro
- `/help` - Hướng dẫn sử dụng

### 2. Chạy Web Dashboard

```bash
streamlit run src/ui/dashboard.py
```

### 3. Chạy Bot chính

```bash
python src/main.py
```

### 4. Demo các tính năng

```bash
# Demo AI Advisor
python demo_ai_advisor.py

# Demo FinGPT Model
python demo_fingpt_model.py

# Demo GPT Assistant
python demo_gpt_assistant.py
```

## 📁 Cấu trúc dự án

```
AlphaPulseBot/
├── 📁 src/                    # Source code chính
│   ├── 📁 ai/                 # AI models và advisors
│   │   ├── fingpt_model.py    # FinGPT model
│   │   ├── gpt_assistant.py   # GPT assistant
│   │   └── investment_advisor.py
│   ├── 📁 analysis/           # Phân tích kỹ thuật
│   │   └── technical_analysis.py
│   ├── 📁 bot/                # Telegram bot
│   │   └── telegram_bot.py
│   ├── 📁 data/               # Thu thập và xử lý dữ liệu
│   ├── 📁 ml/                 # Machine learning models
│   │   └── prediction_models.py
│   ├── 📁 risk/               # Quản lý rủi ro
│   │   └── risk_manager.py
│   ├── 📁 ui/                 # Giao diện người dùng
│   │   └── dashboard.py
│   └── main.py                # Entry point chính
├── 📁 config/                 # Cấu hình
├── 📁 data/                   # Dữ liệu lưu trữ
├── 📁 models/                 # ML models đã train
├── 📁 notebooks/              # Jupyter notebooks
├── 📁 scripts/                # Scripts training
├── 📁 tests/                  # Unit tests
├── 📁 docs/                   # Tài liệu
├── run_telegram_bot.py        # Script chạy Telegram bot
├── requirements.txt           # Dependencies
└── config.env.example         # File cấu hình mẫu
```

## 🔧 Tính năng nâng cao

### Training Models

```bash
# Training FinGPT model
python scripts/finetune_fingpt.py

# Training GPT Assistant
python scripts/finetune_gpt_assistant.py
```

### Debug và Testing

```bash
# Debug Ollama
python debug_ollama.py

# Test GPT Assistant
python test_gpt_assistant_ollama.py
```

## 📊 Ví dụ sử dụng

### Phân tích cổ phiếu VNM

```python
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels

# Khởi tạo
analyzer = TechnicalAnalyzer()
predictor = PredictionModels()

# Phân tích kỹ thuật
data = get_stock_data("VNM")
signals = analyzer.get_trading_signals(data)

# Dự báo AI
prediction = predictor.predict(data, "VNM", "lstm")
```

### Tối ưu Portfolio

```python
from src.risk.risk_manager import RiskManager

risk_manager = RiskManager()
portfolio = ["VNM", "TCB", "HPG", "FPT"]
optimized = risk_manager.optimize_portfolio(portfolio)
```

## 🛡️ Disclaimer

⚠️ **Cảnh báo quan trọng:**

- Đây là dự án **nghiên cứu và giáo dục**
- **KHÔNG** sử dụng cho mục đích đầu tư thực tế mà không có sự tư vấn chuyên môn
- Kết quả phân tích chỉ mang tính chất tham khảo
- Luôn thực hiện due diligence trước khi đầu tư

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ

- **Email**: nhanht2@rikkeisoft.com
- **Division**: RKH
- **Project**: AlphaPulseBot

---

⭐ **Nếu dự án này hữu ích, hãy cho chúng tôi một star!**
