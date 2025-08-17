"""
Base Commands Class
Base class cho tất cả bot commands
"""

from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

class BaseCommands(ABC):
    """Base class cho tất cả bot commands"""
    
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.logger = bot_instance.logger
        
        # Access to core services
        self.trading_service = bot_instance.trading_service
        self.market_service = bot_instance.market_service
        self.config_service = bot_instance.config_service
        
        # Access to legacy components for backward compatibility
        self.vn_collector = bot_instance.trading_service.vn_collector
        self.us_collector = bot_instance.trading_service.us_collector
        self.analyzer = bot_instance.trading_service.analyzer
        self.fundamental_analyzer = bot_instance.trading_service.fundamental_analyzer
        self.sentiment_analyzer = bot_instance.trading_service.sentiment_analyzer
        self.advanced_analyzer = bot_instance.trading_service.advanced_analyzer
        self.options_analyzer = bot_instance.trading_service.options_analyzer
        self.backtester = bot_instance.trading_service.backtester
        self.predictor = bot_instance.trading_service.predictor
        self.risk_manager = bot_instance.trading_service.risk_manager
        self.ai_advisor = bot_instance.trading_service.ai_advisor
        self.gpt_assistant = bot_instance.trading_service.gpt_assistant
        self.claude_assistant = bot_instance.trading_service.claude_assistant
    
    def _escape_markdown(self, text: str) -> str:
        """Escape special characters for Markdown parsing"""
        escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in escape_chars:
            text = text.replace(char, f'\\{char}')
        
        return text
    
    async def _safe_reply_text(self, update: Update, text: str, parse_mode=ParseMode.MARKDOWN):
        """Safely reply text with Markdown fallback"""
        try:
            await update.message.reply_text(text, parse_mode=parse_mode)
        except Exception as markdown_error:
            # If Markdown parsing fails, escape special characters and try again
            escaped_text = self._escape_markdown(text)
            try:
                await update.message.reply_text(escaped_text, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                # If still fails, send as plain text
                await update.message.reply_text(text, parse_mode=None)
