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
🤖 **FinGPT Bot - Hướng dẫn sử dụng**

🇻🇳 **Chuyên phân tích thị trường Việt Nam**

🧠 **AI Investment Advisor Commands:**
• `/stock <symbol>` - **Phân tích AI toàn diện** (Khuyến nghị + Chiến lược)
  Ví dụ: `/stock VNM`, `/stock TCB`

🔮 **AI Prediction Commands:**
• `/predict <symbol> [model]` - **Dự báo giá với AI**
  Ví dụ: `/predict VNM`, `/predict VNM lstm`, `/predict AAPL ensemble`

🤖 **AI Model Training:**
• `/train <symbol> [model]` - **Training AI model**
  Ví dụ: `/train VNM lstm`, `/train AAPL ensemble`

📊 **Model Management:**
• `/model_status <symbol> [model]` - **Kiểm tra trạng thái model**
  Ví dụ: `/model_status VNM`, `/model_status VNM lstm`

📊 **Technical Analysis Commands:**
• `/stock <symbol>` - Phân tích AI toàn diện

📈 **Portfolio & Risk Commands:**
• `/portfolio <symbols>` - Tối ưu hóa portfolio
• `/risk <symbol>` - Phân tích rủi ro chi tiết

🤖 **AI Assistant Commands:**
• `/ask <question>` - **Hỏi đáp GPT** về tài chính
• `/claude <question>` - **Hỏi đáp Claude AI** về tài chính
• `/explain <indicator>` - **Giải thích chỉ báo** kỹ thuật
• `/tips <topic>` - **Lời khuyên đầu tư**

---

🎯 **AI Advisor Features:**
• **Khuyến nghị:** BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL
• **Độ tin cậy:** 0-100% dựa trên phân tích toàn diện
• **Khung thời gian:** 1-3 tháng / 3-6 tháng / 6-12 tháng
• **Mức rủi ro:** LOW/MEDIUM/HIGH theo tiêu chuẩn VN
• **Tâm lý thị trường:** BULLISH/BEARISH/NEUTRAL
• **Phân tích ngành:** Blue-chip, Mid-cap, Ngân hàng, Tiêu dùng

📋 **Chiến lược đầu tư:**
• Kích thước vị thế
• Chiến lược vào lệnh
• Chiến lược thoát lệnh
• Quản lý rủi ro
• Giá mục tiêu & Stop Loss

---

🔍 **Ví dụ sử dụng AI:**
• `/stock VNM` - AI phân tích VNM (VN)
• `/stock TCB` - AI phân tích TCB (VN)
• `/stock HPG` - AI phân tích HPG (VN)
• `/stock FPT` - AI phân tích FPT (VN)

📊 **Ví dụ phân tích thường:**
• `/stock VNM` - Phân tích AI toàn diện VNM
• `/portfolio VNM,TCB,HPG` - Tối ưu portfolio
• `/risk TCB` - Phân tích rủi ro TCB

🤖 **Ví dụ AI Assistants:**

**GPT Assistant (Ollama - Miễn phí):**
• `/ask RSI là gì?` - Hỏi về RSI
• `/ask Làm thế nào để quản lý rủi ro?` - Hỏi về quản lý rủi ro
• `/ask Chiến lược đầu tư dài hạn?` - Hỏi về chiến lược

**Claude AI (Anthropic - Có phí):**
• `/claude RSI là gì?` - Hỏi Claude về RSI
• `/claude Làm thế nào để quản lý rủi ro?` - Hỏi Claude về quản lý rủi ro
• `/claude Phân tích xu hướng thị trường VN?` - Phân tích thị trường
• `/claude So sánh cổ phiếu VNM và TCB?` - So sánh cổ phiếu

**Chung cho cả hai:**
• `/explain MACD` - Giải thích chỉ báo MACD
• `/explain Bollinger` - Giải thích Bollinger Bands
• `/tips general` - Lời khuyên chung
• `/tips technical` - Lời khuyên kỹ thuật
• `/tips risk` - Lời khuyên quản lý rủi ro

📊 **Cổ phiếu VN phổ biến:**
• **Blue-chip:** VNM, TCB, HPG, FPT, VIC, VHM
• **Mid-cap:** VRE, MWG, VPB, ACB, BID, VCB
• **Ngành ngân hàng:** TCB, VPB, ACB, BID, VCB
• **Ngành tiêu dùng:** VNM, MWG, VRE
• **Ngành công nghệ:** FPT
• **Ngành bất động sản:** VIC, VHM

💡 **Lệnh khác:**
• `/start` - Khởi động bot
• `/help` - Hiển thị hướng dẫn này

💡 **Cách sử dụng hiệu quả:**
1. **Bắt đầu với AI Advisor:** `/stock VNM` để có phân tích toàn diện
2. **Tìm hiểu kỹ thuật:** `/explain RSI` để hiểu chỉ báo
3. **Hỏi đáp:** `/ask Làm thế nào để quản lý rủi ro?`
4. **Lời khuyên:** `/tips risk` để có gợi ý đầu tư
5. **Tối ưu portfolio:** `/portfolio VNM,TCB,HPG`

---
🤖 **AI Advisor sử dụng:**
• Phân tích kỹ thuật (35%) - RSI, MACD, Bollinger Bands
• Chỉ số rủi ro (25%) - Sharpe, VaR, Max Drawdown
• Hành động giá (20%) - Support/Resistance, Volume
• Tâm lý thị trường (15%) - Blue-chip, Sector analysis
• Phân tích khối lượng (5%) - Volume trends

🤖 **AI Assistants có thể:**

**GPT Assistant (Ollama):**
• Giải thích các chỉ báo kỹ thuật chi tiết
• Trả lời câu hỏi về tài chính và đầu tư
• Đưa ra lời khuyên đầu tư theo chủ đề
• Phân tích từ khóa thông minh
• Hỗ trợ học tập và nghiên cứu
• **Ưu điểm:** Miễn phí, chạy offline, tốc độ nhanh

**Claude AI (Anthropic):**
• Phân tích tài chính chuyên sâu với độ chính xác cao
• Trả lời câu hỏi phức tạp về thị trường Việt Nam
• So sánh và đánh giá cổ phiếu chi tiết
• Phân tích xu hướng thị trường toàn diện
• Đưa ra khuyến nghị đầu tư thông minh
• **Ưu điểm:** Độ chính xác cao, kiến thức cập nhật, trả lời chi tiết
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all incoming messages"""
        # Just acknowledge the message
        pass
