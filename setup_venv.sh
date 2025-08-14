#!/bin/bash

echo "🔧 Setting up Virtual Environment for AlphaPulse Bot..."

# Kiểm tra venv có tồn tại không
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating new virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Kiểm tra venv đã active chưa
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Cài đặt dependencies
echo "📥 Installing dependencies..."

# Core dependencies
pip install anthropic>=0.7.0
pip install python-dotenv python-telegram-bot
pip install yfinance alpha-vantage ta scikit-learn

# Fix protobuf version mismatch before installing tensorflow
echo "🔧 Fixing protobuf version compatibility..."
pip uninstall -y protobuf google-protobuf
pip install protobuf==4.25.3
pip install tensorflow>=2.15.0 pandas-ta

# Kiểm tra cài đặt
echo "🔍 Checking installations..."
pip list | grep -E "(anthropic|python-dotenv|python-telegram-bot|tensorflow|yfinance)"

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To run the bot:"
echo "   source venv/bin/activate && python3 run_telegram_bot.py"
echo ""
echo "🧪 To test Claude:"
echo "   source venv/bin/activate && python3 test_claude_command.py"
echo ""
echo "📚 For help:"
echo "   source venv/bin/activate && python3 run_telegram_bot.py"
echo "   Then send /help in Telegram" 