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

from src.data.vn_alternative_collector import VNAlternativeCollector
from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager
from src.ai.investment_advisor import AIInvestmentAdvisor
from src.ai.gpt_assistant import GPTAssistant
from src.ai.fingpt_model import FinGPTModel
from src.ai.claude_assistant import ClaudeAssistant

# Import modular commands
from .commands import (
    AICommands,
    PredictionCommands,
    PortfolioCommands,
    AssistantCommands,
    UtilityCommands,
    ButtonHandlers
)

class FinGPTTelegramBot:
    """Modular Telegram Bot cho FinGPT"""
    
    def __init__(self, token: str):
        self.token = token
        self.logger = logging.getLogger(__name__)
        
        # Initialize FinGPT components
        self.vn_collector = VNAlternativeCollector()
        self.us_collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.predictor = PredictionModels()
        self.risk_manager = RiskManager()
        self.ai_advisor = AIInvestmentAdvisor()
        self.gpt_assistant = GPTAssistant(model_name="gpt_assistant:latest")  # Ollama model
        self.fingpt_model = FinGPTModel()  # Custom FinGPT model
        
        # Initialize Claude Assistant
        try:
            self.claude_assistant = ClaudeAssistant()
            self.logger.info("Claude Assistant initialized successfully")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Claude Assistant: {e}")
            self.claude_assistant = None
        
        # User sessions and tracking
        self.user_sessions = {}
        self.welcomed_users = set()  # Track users who have been welcomed
        
        # Initialize modular command handlers
        self._init_command_handlers()
    
    def _init_command_handlers(self):
        """Initialize all command handlers"""
        # Initialize command classes with bot instance
        self.ai_commands = AICommands(self)
        self.prediction_commands = PredictionCommands(self)
        self.portfolio_commands = PortfolioCommands(self)
        self.assistant_commands = AssistantCommands(self)
        self.utility_commands = UtilityCommands(self)
        self.button_handlers = ButtonHandlers(self)
    
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
        
        # Prediction Commands
        application.add_handler(CommandHandler("predict", self.prediction_commands.predict_command))
        application.add_handler(CommandHandler("train", self.prediction_commands.train_command))
        application.add_handler(CommandHandler("model_status", self.prediction_commands.model_status_command))
        
        # Portfolio Commands
        application.add_handler(CommandHandler("portfolio", self.portfolio_commands.portfolio_command))
        application.add_handler(CommandHandler("risk", self.portfolio_commands.risk_command))
        
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
