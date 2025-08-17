"""
Modular Telegram Bot Handler for FinGPT
Bot Telegram với cấu trúc modular cho dễ quản lý và debug
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Import FinGPT modules
import sys
sys.path.append('src')

# Import core services
from src.core.services import TradingService, MarketService, ConfigurationService

# Import modular commands
from .commands.factory import CommandFactory

class FinGPTTelegramBot:
    """Modular Telegram Bot cho FinGPT"""
    
    def __init__(self, token: str):
        self.token = token
        self.logger = logging.getLogger(__name__)
        
        # Initialize core services
        self.trading_service = TradingService()
        self.market_service = MarketService(self.trading_service)
        self.config_service = ConfigurationService()
        
        # User sessions and tracking
        self.user_sessions = {}
        self.welcomed_users = set()  # Track users who have been welcomed
        
        # Initialize command factory
        self.command_factory = CommandFactory()
        
        # Initialize modular command handlers
        self._init_command_handlers()
    
    def _init_command_handlers(self):
        """Initialize all command handlers using factory"""
        # Get all command instances
        all_commands = self.command_factory.get_all_commands(self)
        
        # Assign to instance variables
        self.ai_commands = all_commands['ai']
        self.prediction_commands = all_commands['prediction']
        self.portfolio_commands = all_commands['portfolio']
        self.assistant_commands = all_commands['assistant']
        self.utility_commands = all_commands['utility']
        self.button_handlers = all_commands['button']
        self.fundamental_commands = all_commands['fundamental']
        self.sentiment_commands = all_commands['sentiment']
        self.backtest_commands = all_commands['backtest']
        self.advanced_commands = all_commands['advanced']
    
    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Add command handlers
        self._add_command_handlers(application)
        
        # Add button callback handler
        application.add_handler(CallbackQueryHandler(self.button_handlers.button_callback))
        
        # Add handler for all messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.utility_commands.handle_all_messages))
        
        # Start bot
        self.logger.info("🤖 FinGPT Modular Telegram Bot đang khởi động...")
        application.run_polling()
    
    def _add_command_handlers(self, application):
        """Add all command handlers to application"""
        
        # AI Commands
        application.add_handler(CommandHandler("stock", self.ai_commands.stock_command))
        application.add_handler(CommandHandler("quick", self.ai_commands.quick_command))
        application.add_handler(CommandHandler("scan", self.ai_commands.scan_command))
        application.add_handler(CommandHandler("check", self.ai_commands.check_command))
        
        # Prediction Commands
        application.add_handler(CommandHandler("predict", self.prediction_commands.predict_command))
        application.add_handler(CommandHandler("train", self.prediction_commands.train_command))
        application.add_handler(CommandHandler("model_status", self.prediction_commands.model_status_command))
        
        # Portfolio Commands
        application.add_handler(CommandHandler("portfolio", self.portfolio_commands.portfolio_command))
        application.add_handler(CommandHandler("risk", self.portfolio_commands.risk_command))
        
        # Fundamental Commands
        application.add_handler(CommandHandler("fundamental", self.fundamental_commands.fundamental_command))
        application.add_handler(CommandHandler("ratios", self.fundamental_commands.ratios_command))
        application.add_handler(CommandHandler("earnings", self.fundamental_commands.earnings_command))
        
        # Sentiment Commands
        application.add_handler(CommandHandler("sentiment", self.sentiment_commands.sentiment_command))
        application.add_handler(CommandHandler("news", self.sentiment_commands.news_command))
        application.add_handler(CommandHandler("market", self.sentiment_commands.market_command))
        application.add_handler(CommandHandler("sector", self.sentiment_commands.sector_command))
        
        # Backtesting Commands
        application.add_handler(CommandHandler("backtest", self.backtest_commands.backtest_command))
        application.add_handler(CommandHandler("strategy", self.backtest_commands.strategy_command))
        application.add_handler(CommandHandler("performance", self.backtest_commands.performance_command))
        
        # Advanced Technical Commands
        application.add_handler(CommandHandler("fibonacci", self.advanced_commands.fibonacci_command))
        application.add_handler(CommandHandler("elliott", self.advanced_commands.elliott_command))
        application.add_handler(CommandHandler("volume", self.advanced_commands.volume_command))
        application.add_handler(CommandHandler("ichimoku", self.advanced_commands.ichimoku_command))
        application.add_handler(CommandHandler("options", self.advanced_commands.options_command))
        
        # Assistant Commands
        application.add_handler(CommandHandler("ask", self.assistant_commands.ask_command))
        application.add_handler(CommandHandler("claude", self.assistant_commands.claude_command))
        application.add_handler(CommandHandler("explain", self.assistant_commands.explain_command))
        application.add_handler(CommandHandler("tips", self.assistant_commands.tips_command))
        
        # Utility Commands
        application.add_handler(CommandHandler("start", self.utility_commands.start_command))
        application.add_handler(CommandHandler("help", self.utility_commands.help_command))

def main():
    """Main function"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Vui lòng set TELEGRAM_BOT_TOKEN trong environment variables")
        print("Hoặc tạo file .env với nội dung:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    # Create and run bot
    bot = FinGPTTelegramBot(token)
    bot.run()

if __name__ == "__main__":
    main() 
