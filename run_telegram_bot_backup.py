"""
Run FinGPT Telegram Bot
Script để chạy bot Telegram cho FinGPT
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from src.bot.telegram_bot import FinGPTTelegramBot

def main():
    """Main function to run Telegram bot"""
    print("🤖 FinGPT Telegram Bot")
    print("="*50)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check if token exists
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN không được tìm thấy!")
        print("\n🔧 Hướng dẫn tạo bot Telegram:")
        print("1. Mở Telegram và tìm @BotFather")
        print("2. Gửi lệnh /newbot")
        print("3. Đặt tên cho bot (ví dụ: FinGPT Bot)")
        print("4. Đặt username cho bot (ví dụ: fingpt_bot)")
        print("5. BotFather sẽ trả về token")
        print("\n📝 Tạo file .env với nội dung:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        print("\n💡 Ví dụ:")
        print("TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
        return
    
    print("✅ Token đã được tìm thấy!")
    print("🚀 Đang khởi động FinGPT Telegram Bot...")
    print("\n📱 Để sử dụng bot:")
    print("1. Tìm bot của bạn trên Telegram")
    print("2. Gửi lệnh /start để bắt đầu")
    print("3. Sử dụng các lệnh:")
    print("   • /stock VNM - Phân tích cổ phiếu VNM")
    print("   • /stock AAPL - Phân tích cổ phiếu Apple")
    print("   • /portfolio VNM,TCB,HPG - Tối ưu portfolio")
    print("   • /risk VNM - Phân tích rủi ro")
    print("   • /help - Hướng dẫn sử dụng")
    
    try:
        # Create and run bot
        bot = FinGPTTelegramBot(token)
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot đã được dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy bot: {str(e)}")

if __name__ == "__main__":
    main() 