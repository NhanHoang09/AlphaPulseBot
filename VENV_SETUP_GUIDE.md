# Virtual Environment Setup Guide

## 🔧 Hướng dẫn cài đặt Virtual Environment

### ⚠️ Lỗi thường gặp:

```
ModuleNotFoundError: No module named 'anthropic'
```

### ✅ Giải pháp:

#### 1. **Kích hoạt Virtual Environment**

```bash
# Kích hoạt venv
source venv/bin/activate

# Kiểm tra venv đã active chưa
which python
# Kết quả: /Users/username/AlphaPulseBot/venv/bin/python
```

#### 2. **Cài đặt Dependencies trong venv**

```bash
# Đảm bảo venv đã active (thấy (venv) ở đầu prompt)
(venv) $ pip install -r requirements.txt

# Hoặc cài từng package
(venv) $ pip install anthropic>=0.7.0
(venv) $ pip install python-dotenv python-telegram-bot
(venv) $ pip install yfinance alpha-vantage ta scikit-learn
(venv) $ pip install tensorflow
```

#### 3. **Kiểm tra Dependencies**

```bash
# Kiểm tra anthropic đã cài chưa
(venv) $ pip list | grep anthropic

# Kiểm tra tất cả packages
(venv) $ pip list
```

#### 4. **Chạy Bot trong venv**

```bash
# Đảm bảo venv active
(venv) $ python3 run_telegram_bot.py

# Hoặc
(venv) $ python run_telegram_bot.py
```

### 🚀 Script tự động:

#### Tạo file `setup_venv.sh`:

```bash
#!/bin/bash

echo "🔧 Setting up Virtual Environment..."

# Kích hoạt venv
source venv/bin/activate

# Cài đặt dependencies
pip install anthropic>=0.7.0
pip install python-dotenv python-telegram-bot
pip install yfinance alpha-vantage ta scikit-learn
pip install tensorflow pandas-ta

echo "✅ Setup completed!"
echo "🚀 Run: source venv/bin/activate && python3 run_telegram_bot.py"
```

#### Chạy script:

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### 📋 Checklist:

- [ ] Virtual environment đã được tạo
- [ ] venv đã được kích hoạt (thấy `(venv)` ở prompt)
- [ ] `anthropic` package đã được cài đặt
- [ ] `python-dotenv` đã được cài đặt
- [ ] `python-telegram-bot` đã được cài đặt
- [ ] `tensorflow` đã được cài đặt
- [ ] Bot chạy thành công

### 🔍 Troubleshooting:

#### 1. **Lỗi "No module named 'anthropic'"**

```bash
# Giải pháp: Cài đặt trong venv
source venv/bin/activate
pip install anthropic>=0.7.0
```

#### 2. **Lỗi "No module named 'tensorflow'"**

```bash
# Giải pháp: Cài đặt trong venv
source venv/bin/activate
pip install tensorflow
```

#### 3. **Lỗi "No module named 'yfinance'"**

```bash
# Giải pháp: Cài đặt trong venv
source venv/bin/activate
pip install yfinance
```

#### 4. **Kiểm tra venv có active không**

```bash
# Nếu thấy (venv) ở đầu prompt = OK
(venv) $ echo $VIRTUAL_ENV
# Kết quả: /Users/username/AlphaPulseBot/venv
```

### 💡 Tips:

1. **Luôn kích hoạt venv trước khi chạy bot**
2. **Kiểm tra prompt có `(venv)` không**
3. **Cài đặt dependencies trong venv, không phải global**
4. **Sử dụng `pip list` để kiểm tra packages**

### 🎯 Quick Start:

```bash
# 1. Kích hoạt venv
source venv/bin/activate

# 2. Cài dependencies (nếu chưa có)
pip install anthropic python-dotenv python-telegram-bot tensorflow yfinance

# 3. Chạy bot
python3 run_telegram_bot.py
```

---

**Lưu ý**: Luôn đảm bảo virtual environment được kích hoạt trước khi chạy bot để tránh lỗi dependencies!
