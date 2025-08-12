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
🤖 **AlphaPulse Bot here!**

👋 Hello {user.first_name}! I'm your intelligent AI-powered investment assistant, ready to help you invest smarter, manage risk ⚖️, and grow your portfolio 📈💰.

        """
        
        keyboard = [
            [InlineKeyboardButton("🧠 AI Investment Advisor", callback_data="analyze_stock")],
            [InlineKeyboardButton("🔮 AI Prediction", callback_data="ai_prediction")],
            [InlineKeyboardButton("📊 Technical Analysis", callback_data="technical_analysis")],
            [InlineKeyboardButton("🤖 GPT Assistant", callback_data="gpt_assistant")],
            [InlineKeyboardButton("🤖 Claude AI", callback_data="claude_assistant")],
            [InlineKeyboardButton("📊 Portfolio Management", callback_data="portfolio_management")],
            [InlineKeyboardButton("📋 Model Management", callback_data="model_management")],
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
        help_text = """
🤖 **AlphaPulse Bot - Command List**

📋 **Danh sách tất cả commands theo module:**

---

## 🧠 **AI Investment Advisor Module**
**Phân tích AI toàn diện với khuyến nghị và chiến lược đầu tư**

• `/stock <symbol>` - **Phân tích AI toàn diện**
  - Khuyến nghị: BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL
  - Độ tin cậy: 0-100%
  - Chiến lược đầu tư chi tiết
  - Target price & Stop loss
  - Ví dụ: `/stock VNM`, `/stock TCB`, `/stock AAPL`

---

## 🔮 **AI Prediction Module**
**Dự báo giá cổ phiếu với AI models**

• `/predict <symbol> [model]` - **Dự báo giá với AI**
  - Models: `lstm` (mặc định), `ensemble`
  - Ví dụ: `/predict VNM`, `/predict VNM lstm`, `/predict AAPL ensemble`

• `/train <symbol> [model]` - **Training AI model**
  - Training LSTM hoặc Ensemble model
  - Ví dụ: `/train VNM lstm`, `/train VNM ensemble`

• `/model_status <symbol> [model]` - **Kiểm tra trạng thái model**
  - Kiểm tra model đã train hay chưa
  - Ví dụ: `/model_status VNM`, `/model_status VNM lstm`

---

## 📊 **Technical Analysis Module**
**Giải thích và hướng dẫn chỉ báo kỹ thuật**

• `/explain <indicator>` - **Giải thích chỉ báo kỹ thuật**
  - RSI, MACD, Bollinger Bands, Stochastic, Williams %R, ATR
  - Ví dụ: `/explain RSI`, `/explain MACD`, `/explain Bollinger`

---

## 📈 **Portfolio Management Module**
**Quản lý danh mục đầu tư và phân tích rủi ro**

• `/portfolio <symbols>` - **Tối ưu hóa portfolio**
  - Tối ưu trọng số portfolio theo Sharpe ratio
  - Ví dụ: `/portfolio VNM,TCB,HPG`, `/portfolio VNM,TCB,HPG,FPT,VIC`

• `/risk <symbol>` - **Phân tích rủi ro chi tiết**
  - Sharpe ratio, VaR, Max drawdown, Volatility
  - Ví dụ: `/risk VNM`, `/risk TCB`

---

## 🤖 **AI Assistant Module**
**Hỏi đáp và lời khuyên với AI**

• `/ask <question>` - **GPT Assistant (Ollama - Miễn phí)**
  - Hỏi đáp về tài chính và đầu tư
  - Ví dụ: `/ask RSI là gì?`, `/ask Làm thế nào để quản lý rủi ro?`

• `/claude <question>` - **Claude AI (Anthropic - Có phí)**
  - Phân tích chuyên sâu với độ chính xác cao
  - Ví dụ: `/claude Phân tích xu hướng thị trường VN?`

• `/tips <topic>` - **Lời khuyên đầu tư**
  - Topics: `general`, `technical`, `risk`
  - Ví dụ: `/tips general`, `/tips technical`, `/tips risk`

---

## 🔧 **Utility Module**
**Các lệnh tiện ích của bot**

• `/start` - **Khởi động bot**
  - Hiển thị menu chính với các tính năng

• `/help` - **Hướng dẫn sử dụng**
  - Hiển thị danh sách commands này

---

## 📊 **Cổ phiếu phổ biến**

**🇻🇳 Thị trường Việt Nam:**
• **Blue-chip:** VNM, TCB, HPG, FPT, VIC, VHM
• **Mid-cap:** VRE, MWG, VPB, ACB, BID, VCB
• **Ngành ngân hàng:** TCB, VPB, ACB, BID, VCB
• **Ngành tiêu dùng:** VNM, MWG, VRE
• **Ngành công nghệ:** FPT
• **Ngành bất động sản:** VIC, VHM

**🇺🇸 Thị trường Mỹ:**
• **Tech:** AAPL, MSFT, GOOGL, AMZN, TSLA
• **Finance:** JPM, BAC, WFC, GS
• **Healthcare:** JNJ, PFE, UNH

---

## 💡 **Cách sử dụng hiệu quả**

1. **Bắt đầu với AI Advisor:** `/stock VNM` để có phân tích toàn diện
2. **Tìm hiểu kỹ thuật:** `/explain RSI` để hiểu chỉ báo
3. **Dự báo giá:** `/predict VNM` để dự báo xu hướng
4. **Hỏi đáp:** `/ask Làm thế nào để quản lý rủi ro?`
5. **Lời khuyên:** `/tips risk` để có gợi ý đầu tư
6. **Tối ưu portfolio:** `/portfolio VNM,TCB,HPG`

---

## 🎯 **Tổng cộng: 12 Commands**

**🧠 AI Investment Advisor:** 1 command
**🔮 AI Prediction:** 3 commands  
**📊 Technical Analysis:** 1 command
**📈 Portfolio Management:** 2 commands
**🤖 AI Assistant:** 3 commands
**🔧 Utility:** 2 commands

---
💡 **Lưu ý:** Sử dụng `/start` để xem menu chính với các tính năng
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all incoming messages"""
        # Just acknowledge the message
        pass
