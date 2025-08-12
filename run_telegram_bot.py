#!/usr/bin/env python3
"""
Run Modular Telegram Bot
Script để chạy Telegram Bot với cấu trúc modular
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from src.bot.telegram_bot import FinGPTTelegramBot

def main():
    """Main function"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Vui lòng set TELEGRAM_BOT_TOKEN trong environment variables")
        print("Hoặc tạo file .env với nội dung:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    print("🤖 Khởi động FinGPT Telegram Bot...")
    
    # Create and run bot
    bot = FinGPTTelegramBot(token)
    bot.run()

if __name__ == "__main__":
    main()
