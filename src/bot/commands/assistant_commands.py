"""
AI Assistant Commands
Commands cho GPT và Claude AI assistants
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class AssistantCommands(BaseCommands):
    """AI Assistant Commands"""
    
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ask command for GPT Assistant"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập câu hỏi!\n"
                "Ví dụ: `/ask RSI là gì?`\n"
                "Ví dụ: `/ask Làm thế nào để quản lý rủi ro?`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        question = " ".join(context.args)
        await self.ask_gpt(update, context, question)
    
    async def claude_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /claude command for Claude AI Assistant"""
        if not self.claude_assistant:
            await update.message.reply_text(
                "❌ Claude AI Assistant chưa được khởi tạo!\n"
                "Vui lòng kiểm tra ANTHROPIC_API_KEY trong file config.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
            
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập câu hỏi!\n"
                "Ví dụ: `/claude RSI là gì?`\n"
                "Ví dụ: `/claude Làm thế nào để quản lý rủi ro?`\n"
                "Ví dụ: `/claude Phân tích xu hướng thị trường VN?`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        question = " ".join(context.args)
        await self.ask_claude(update, context, question)
    
    async def explain_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /explain command for technical indicators"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập chỉ báo cần giải thích!\n"
                "Ví dụ: `/explain RSI`\n"
                "Ví dụ: `/explain MACD`\n"
                "Ví dụ: `/explain Bollinger`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        indicator = context.args[0].upper()
        await self.explain_indicator(update, context, indicator)
    
    async def tips_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tips command for investment tips"""
        topic = context.args[0] if context.args else "general"
        await self.get_investment_tips(update, context, topic)
    
    async def ask_gpt(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question: str):
        """Ask GPT Assistant a question"""
        try:
            await update.message.reply_text(f"🤖 Đang phân tích câu hỏi: {question}")
            
            # Get answer from GPT Assistant
            analysis = self.gpt_assistant.analyze_question(question)
            response = self.gpt_assistant.format_response(analysis)
            
            # Add confidence level
            confidence = analysis.get('confidence', 0)
            confidence_text = f"📊 **Độ tin cậy:** {confidence:.1%}\n\n"
            
            full_response = confidence_text + response
            
            # Use safe reply with Markdown fallback
            await self._safe_reply_text(update, full_response)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi xử lý câu hỏi: {str(e)}")
    
    async def ask_claude(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question: str):
        """Ask Claude AI Assistant a question"""
        try:
            await update.message.reply_text(f"🤖 Claude AI đang phân tích: {question}")
            
            # Get answer from Claude Assistant
            analysis = self.claude_assistant.analyze_question(question)
            response = self.claude_assistant.format_response(analysis)
            
            # Use safe reply with Markdown fallback
            await self._safe_reply_text(update, response)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi xử lý câu hỏi với Claude: {str(e)}")
    
    async def explain_indicator(self, update: Update, context: ContextTypes.DEFAULT_TYPE, indicator: str):
        """Explain a technical indicator"""
        try:
            await update.message.reply_text(f"📚 Đang giải thích chỉ báo: {indicator}")
            
            # Get explanation from GPT Assistant
            explanation = self.gpt_assistant.explain_indicator(indicator)
            
            if 'error' in explanation:
                await update.message.reply_text(f"❌ {explanation['error']}")
                return
            
            # Format explanation based on available fields
            message = f"""
📊 **{explanation['indicator']} - {explanation['name']}**

📝 **Mô tả:**
{explanation['description']}
"""
            
            # Add optional fields if they exist
            if 'interpretation' in explanation:
                message += f"\n🎯 **Cách hiểu:**\n{explanation['interpretation']}\n"
            
            if 'calculation' in explanation:
                message += f"\n🧮 **Công thức tính:**\n{explanation['calculation']}\n"
            
            if 'usage' in explanation:
                message += f"\n💡 **Cách sử dụng:**\n{explanation['usage']}\n"
            
            # Add source info if available
            if 'source' in explanation and explanation['source'] != 'fallback':
                message += f"\n🤖 **Nguồn:** {explanation.get('model_version', 'AI Model')}"
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi giải thích chỉ báo: {str(e)}")
    
    async def get_investment_tips(self, update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
        """Get investment tips"""
        try:
            await update.message.reply_text(f"💡 Đang tìm lời khuyên đầu tư về: {topic}")
            
            # Get tips from GPT Assistant
            tips = self.gpt_assistant.get_investment_tips(topic)
            
            # Format tips
            topic_names = {
                "general": "Chung",
                "technical": "Kỹ thuật",
                "risk": "Quản lý rủi ro"
            }
            
            topic_name = topic_names.get(topic, topic.title())
            
            message = f"""
💡 **Lời khuyên đầu tư - {topic_name}**

"""
            
            for i, tip in enumerate(tips, 1):
                message += f"{i}. {tip}\n"
            
            message += f"\n💡 **Sử dụng:** `/tips general`, `/tips technical`, `/tips risk`"
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi lấy lời khuyên: {str(e)}")
