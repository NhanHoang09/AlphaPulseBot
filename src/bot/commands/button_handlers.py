"""
Button Handlers
Handlers cho button callbacks
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class ButtonHandlers(BaseCommands):
    """Button Callback Handlers"""
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "analyze_stock":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "🧠 **AI Investment Advisor**\n\n"
                "**Lệnh AI toàn diện:**\n"
                "• `/stock VNM` - AI phân tích VNM (Khuyến nghị + Chiến lược)\n"
                "• `/stock AAPL` - AI phân tích Apple (Khuyến nghị + Chiến lược)\n"
                "• `/stock TCB` - AI phân tích TCB (Khuyến nghị + Chiến lược)\n\n"
                "🤖 **AI Advisor bao gồm:**\n"
                "• Khuyến nghị: BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL\n"
                "• Độ tin cậy: 0-100%\n"
                "• Chiến lược đầu tư chi tiết\n"
                "• Target price & Stop loss",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "ai_prediction":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "🔮 **AI Prediction - Dự báo giá với AI**\n\n"
                "**Lệnh dự báo:**\n"
                "• `/predict <symbol> [model]` - Dự báo giá\n"
                "• `/train <symbol> [model]` - Training model\n"
                "• `/model_status <symbol>` - Kiểm tra model\n\n"
                "**Ví dụ sử dụng:**\n"
                "• `/predict VNM` - Dự báo VNM với LSTM\n"
                "• `/predict VNM ensemble` - Dự báo VNM với Ensemble\n"
                "• `/predict AAPL` - Dự báo cổ phiếu Mỹ\n"
                "• `/train VNM lstm` - Training LSTM cho VNM\n"
                "• `/model_status VNM` - Kiểm tra model VNM\n\n"
                "**Lưu ý:**\n"
                "• Cần train model trước khi dự báo\n"
                "• LSTM: Dự báo dựa trên time series\n"
                "• Ensemble: Kết hợp nhiều thuật toán",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "technical_analysis":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "📊 **Technical Analysis - Phân tích kỹ thuật**\n\n"
                "**Lệnh phân tích:**\n"
                "• `/explain <indicator>` - Giải thích chỉ báo kỹ thuật\n\n"
                "**Chỉ báo kỹ thuật:**\n"
                "• RSI - Relative Strength Index\n"
                "• MACD - Moving Average Convergence Divergence\n"
                "• Bollinger Bands - Dải Bollinger\n"
                "• Moving Averages - Đường trung bình\n"
                "• Volume - Khối lượng giao dịch\n"
                "• Stochastic - Stochastic Oscillator\n"
                "• Williams %R - Williams Percent Range\n"
                "• ATR - Average True Range\n\n"
                "**Ví dụ sử dụng:**\n"
                "• `/explain RSI` - Giải thích RSI\n"
                "• `/explain MACD` - Giải thích MACD\n"
                "• `/explain Bollinger` - Giải thích Bollinger Bands\n"
                "• `/explain Stochastic` - Giải thích Stochastic\n\n"
                "💡 **Lưu ý:** Phân tích AI toàn diện sử dụng lệnh `/stock <symbol>` trong AI Investment Advisor",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "portfolio_management":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "📊 **Portfolio Management - Quản lý danh mục**\n\n"
                "**Lệnh quản lý:**\n"
                "• `/portfolio <symbols>` - Tối ưu hóa portfolio\n"
                "• `/risk <symbol>` - Phân tích rủi ro\n\n"
                "**Tính năng:**\n"
                "• Tối ưu hóa trọng số portfolio\n"
                "• Phân tích rủi ro chi tiết\n"
                "• Sharpe ratio, VaR, Max drawdown\n"
                "• Cảnh báo rủi ro tự động\n\n"
                "**Ví dụ sử dụng:**\n"
                "• `/portfolio VNM,TCB,HPG` - Tối ưu 3 cổ phiếu\n"
                "• `/portfolio VNM,TCB,HPG,FPT,VIC` - Tối ưu 5 cổ phiếu\n"
                "• `/risk VNM` - Phân tích rủi ro VNM",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "model_management":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "📋 **Model Management - Quản lý AI Models**\n\n"
                "**Lệnh quản lý:**\n"
                "• `/train <symbol> [model]` - Training model\n"
                "• `/model_status <symbol> [model]` - Kiểm tra model\n"
                "• `/predict <symbol> [model]` - Dự báo với model\n\n"
                "**Loại models:**\n"
                "• LSTM - Long Short-Term Memory\n"
                "• Ensemble - Kết hợp nhiều thuật toán\n\n"
                "**Ví dụ sử dụng:**\n"
                "• `/train VNM lstm` - Training LSTM cho VNM\n"
                "• `/train VNM ensemble` - Training Ensemble cho VNM\n"
                "• `/model_status VNM` - Kiểm tra tất cả models\n"
                "• `/predict VNM lstm` - Dự báo với LSTM",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "gpt_assistant":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "🤖 **GPT Assistant - Hỏi đáp thông minh**\n\n"
                "**Lệnh GPT Assistant:**\n"
                "• `/ask <câu hỏi>` - **Hỏi đáp AI** về tài chính\n"
                "• `/explain <chỉ báo>` - **Giải thích chỉ báo** kỹ thuật\n"
                "• `/tips <chủ đề>` - **Lời khuyên đầu tư**\n\n"
                "**Ví dụ sử dụng:**\n"
                "• `/ask RSI là gì?` - Hỏi về chỉ báo RSI\n"
                "• `/ask Làm thế nào để quản lý rủi ro?` - Hỏi về quản lý rủi ro\n"
                "• `/explain MACD` - Giải thích chỉ báo MACD\n"
                "• `/explain Bollinger` - Giải thích Bollinger Bands\n"
                "• `/tips general` - Lời khuyên chung\n"
                "• `/tips technical` - Lời khuyên kỹ thuật\n"
                "• `/tips risk` - Lời khuyên quản lý rủi ro\n\n"
                "**Tính năng:**\n"
                "• Trả lời mọi câu hỏi về tài chính\n"
                "• Giải thích chi tiết các chỉ báo kỹ thuật\n"
                "• Đưa ra lời khuyên đầu tư thông minh\n"
                "• Sử dụng AI Ollama để xử lý",
                reply_markup=reply_markup
            )
        elif query.data == "claude_assistant":
            keyboard = [
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if not self.claude_assistant:
                await query.edit_message_text(
                    "❌ **Claude AI Assistant chưa sẵn sàng**\n\n"
                    "**Lý do:**\n"
                    "• ANTHROPIC_API_KEY chưa được cấu hình\n"
                    "• Hoặc API key không hợp lệ\n\n"
                    "**Cách khắc phục:**\n"
                    "1. Đăng ký tài khoản tại https://console.anthropic.com\n"
                    "2. Tạo API key\n"
                    "3. Thêm vào file config.env:\n"
                    "   `ANTHROPIC_API_KEY=your_api_key_here`\n"
                    "4. Khởi động lại bot",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    "🤖 **Claude AI Assistant - AI thông minh**\n\n"
                    "**Lệnh Claude AI:**\n"
                    "• `/claude <câu hỏi>` - **Hỏi đáp Claude AI** về tài chính\n"
                    "• `/explain <chỉ báo>` - **Giải thích chỉ báo** kỹ thuật\n"
                    "• `/tips <chủ đề>` - **Lời khuyên đầu tư**\n\n"
                    "**Ví dụ sử dụng:**\n"
                    "• `/claude RSI là gì?` - Hỏi về chỉ báo RSI\n"
                    "• `/claude Làm thế nào để quản lý rủi ro?` - Hỏi về quản lý rủi ro\n"
                    "• `/claude Phân tích xu hướng thị trường VN?` - Phân tích thị trường\n"
                    "• `/explain MACD` - Giải thích chỉ báo MACD\n"
                    "• `/explain Bollinger` - Giải thích Bollinger Bands\n"
                    "• `/tips general` - Lời khuyên chung\n"
                    "• `/tips technical` - Lời khuyên kỹ thuật\n"
                    "• `/tips risk` - Lời khuyên quản lý rủi ro\n\n"
                    "**Tính năng:**\n"
                    "• Trả lời mọi câu hỏi về tài chính\n"
                    "• Giải thích chi tiết các chỉ báo kỹ thuật\n"
                    "• Đưa ra lời khuyên đầu tư thông minh\n"
                    "• Sử dụng Claude 3.5 Sonnet API\n"
                    "• Độ tin cậy cao, trả lời chi tiết",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        elif query.data == "back_to_main":
            # Return to main menu
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
            
            await query.edit_message_text(
                welcome_message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
