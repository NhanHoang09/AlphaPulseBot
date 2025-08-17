"""
Utility Commands
Commands cho utility functions (start, help, buttons)
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class UtilityCommands(BaseCommands):
    """Utility Commands"""
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"""
🤖 **AlphaPulse Trading Bot v2.0**

👋 Hello {user.first_name}! I'm your professional trading assistant.

🎯 **Tôi sẽ giúp bạn:**
• Phân tích thị trường toàn diện
• Tìm cổ phiếu tiềm năng  
• Đưa ra quyết định đầu tư thông minh
• Quản lý rủi ro hiệu quả

💡 **Quick Start Commands:**
• `/scan <symbol>` - Quick analysis (30s)
• `/check <symbol>` - Deep analysis (2 phút)
• `/risk <symbol>` - Risk analysis

📊 **Popular Stocks:**
🇻🇳 VNM, TCB, HPG, FPT | 🇺🇸 AAPL, MSFT, GOOGL, TSLA

📋 **Chọn phần bạn muốn xem chi tiết:**
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Core Services", callback_data="help_core")],
            [InlineKeyboardButton("🔍 Analysis Module", callback_data="help_analysis")],
            [InlineKeyboardButton("📊 Portfolio & Strategy", callback_data="help_portfolio")],
            [InlineKeyboardButton("🤖 AI Module", callback_data="help_ai")],
            [InlineKeyboardButton("📋 Model Management", callback_data="help_model")],
            [InlineKeyboardButton("🏗️ Architecture", callback_data="help_architecture")],
            [InlineKeyboardButton("💡 Workflow Tips", callback_data="help_workflow")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        # Mark user as welcomed
        user_id = update.effective_user.id
        self.bot.welcomed_users.add(user_id)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        # Tạo keyboard cho các phần help
        keyboard = [
            [InlineKeyboardButton("⚡ Core Services", callback_data="help_core")],
            [InlineKeyboardButton("🔍 Analysis Module", callback_data="help_analysis")],
            [InlineKeyboardButton("📊 Portfolio & Strategy", callback_data="help_portfolio")],
            [InlineKeyboardButton("🤖 AI Module", callback_data="help_ai")],
            [InlineKeyboardButton("📋 Model Management", callback_data="help_model")],
            [InlineKeyboardButton("🏗️ Architecture", callback_data="help_architecture")],
            [InlineKeyboardButton("💡 Workflow Tips", callback_data="help_workflow")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🤖 **AlphaPulse Trading Bot v2.0 - Professional Commands**

📋 **Commands được sắp xếp theo MODULE ARCHITECTURE**

**Chọn phần bạn muốn xem chi tiết:**

⚡ **Core Services** - Commands chính (80% usage)
🔍 **Analysis Module** - Tất cả phân tích (15% usage)  
📊 **Portfolio & Strategy** - Quản lý danh mục
🤖 **AI Module** - AI assistants
📋 **Model Management** - Quản lý AI models
🏗️ **Architecture** - Kiến trúc hệ thống
💡 **Workflow Tips** - Tips cho trader

**💡 Quick Start:**
• `/scan <symbol>` - Quick analysis (alias: `/quick`)
• `/check <symbol>` - Deep analysis (alias: `/stock`)
• `/risk <symbol>` - Risk analysis

**📊 Popular Stocks:**
🇻🇳 VNM, TCB, HPG, FPT | 🇺🇸 AAPL, MSFT, GOOGL, TSLA
        """
        
        await update.message.reply_text(
            help_text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all incoming messages"""
        # Just acknowledge the message
        pass
