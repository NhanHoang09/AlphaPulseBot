"""
Telegram Bot Handler for FinGPT
Bot Telegram cho phân tích tài chính và dự báo thị trường
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

class FinGPTTelegramBot:
    """Telegram Bot cho FinGPT"""
    
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
        
        # User sessions and tracking
        self.user_sessions = {}
        self.welcomed_users = set()  # Track users who have been welcomed
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"""
🤖 **AlphaPulse Bot here!**

👋 Hello {user.first_name}! I’m your intelligent AI-powered investment assistant, ready to help you invest smarter, manage risk ⚖️, and grow your portfolio 📈💰.

        """
        
        keyboard = [
            [InlineKeyboardButton("🧠 AI Investment Advisor", callback_data="analyze_stock")],
            [InlineKeyboardButton("🤖 GPT Assistant", callback_data="gpt_assistant")],
            [InlineKeyboardButton("📊 Tối ưu Portfolio", callback_data="optimize_portfolio")],
            [InlineKeyboardButton("⚠️ Phân tích rủi ro", callback_data="risk_analysis")],
            [InlineKeyboardButton("🇻🇳 Thị trường VN", callback_data="vn_market")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        # Mark user as welcomed
        user_id = update.effective_user.id
        self.welcomed_users.add(user_id)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **FinGPT Bot - Hướng dẫn sử dụng**

🇻🇳 **Chuyên phân tích thị trường Việt Nam**

🧠 **AI Investment Advisor Commands:**
• `/stock <symbol>` - **Phân tích AI toàn diện** (Khuyến nghị + Chiến lược)
  Ví dụ: `/stock VNM`, `/stock TCB`

📊 **Technical Analysis Commands:**
• `/vn <symbol>` - Phân tích kỹ thuật VN

📈 **Portfolio & Risk Commands:**
• `/portfolio <symbols>` - Tối ưu hóa portfolio
• `/risk <symbol>` - Phân tích rủi ro chi tiết

🤖 **GPT Assistant Commands:**
• `/ask <question>` - **Hỏi đáp AI** về tài chính
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
• `/vn VNM` - Chỉ phân tích kỹ thuật VNM
• `/vn TCB` - Chỉ phân tích kỹ thuật TCB
• `/portfolio VNM,TCB,HPG` - Tối ưu portfolio
• `/risk TCB` - Phân tích rủi ro TCB

🤖 **Ví dụ GPT Assistant:**
• `/ask RSI là gì?` - Hỏi về RSI
• `/ask Làm thế nào để quản lý rủi ro?` - Hỏi về quản lý rủi ro
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

🤖 **GPT Assistant có thể:**
• Giải thích các chỉ báo kỹ thuật chi tiết
• Trả lời câu hỏi về tài chính và đầu tư
• Đưa ra lời khuyên đầu tư theo chủ đề
• Phân tích từ khóa thông minh
• Hỗ trợ học tập và nghiên cứu
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def stock_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stock command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập mã cổ phiếu!\n"
                "Ví dụ: `/stock VNM` hoặc `/stock AAPL`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbol = context.args[0].upper()
        await self.analyze_stock_with_ai(update, context, symbol)
    
    async def vn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vn command for Vietnam market"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập mã cổ phiếu VN!\n"
                "Ví dụ: `/vn VNM` hoặc `/vn TCB`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbol = context.args[0].upper()
        await self.analyze_vn_stock(update, context, symbol)
    
    async def us_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /us command for US market (temporarily disabled)"""
        await update.message.reply_text(
            "⚠️ **Thị trường Mỹ tạm thời không khả dụng**\n\n"
            "Thị trường Mỹ đang được bảo trì.\n"
            "Vui lòng sử dụng thị trường Việt Nam:\n"
            "• `/vn VNM` - Phân tích VNM\n"
            "• `/vn TCB` - Phân tích TCB\n"
            "• `/vn HPG` - Phân tích HPG",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /portfolio command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập danh sách cổ phiếu!\n"
                "Ví dụ: `/portfolio VNM,TCB,HPG`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbols = [s.strip().upper() for s in context.args[0].split(',')]
        await self.optimize_portfolio(update, context, symbols)
    
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /risk command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Vui lòng nhập mã cổ phiếu!\n"
                "Ví dụ: `/risk VNM`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbol = context.args[0].upper()
        await self.analyze_risk(update, context, symbol)
    
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
    
    async def analyze_stock_with_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze stock with AI advisor (VN market only)"""
        await update.message.reply_text(f"🤖 Đang phân tích {symbol} với AI Advisor...")
        
        # Try VN market only
        data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
        if not data.empty:
            await self.analyze_vn_stock_with_ai(update, context, symbol)
        else:
            await update.message.reply_text(f"❌ Không tìm thấy dữ liệu cho {symbol} trên thị trường VN")
    
    async def analyze_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze stock (VN market only) - Legacy method"""
        await update.message.reply_text(f"🔍 Đang phân tích {symbol}...")
        
        # Try VN market only
        data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
        if not data.empty:
            await self.analyze_vn_stock(update, context, symbol)
        else:
            await update.message.reply_text(f"❌ Không tìm thấy dữ liệu cho {symbol} trên thị trường VN")
    
    async def analyze_vn_stock_with_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze Vietnam stock with AI advisor"""
        try:
            # Get data
            data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # AI recommendation
            recommendation = self.ai_advisor.generate_recommendation(
                symbol, data, signals, risk_report, "VN"
            )
            
            # Investment strategy
            strategy = self.ai_advisor.get_investment_strategy(recommendation)
            
            # Build AI message
            message = f"""
🤖 **AI Investment Advisor - {symbol} (VN)**

💰 **Giá hiện tại:** {current_price:,.0f} VND
📈 **Thay đổi:** {change:+.2f}%

🎯 **Khuyến nghị AI:** {recommendation.recommendation}
📊 **Độ tin cậy:** {recommendation.confidence:.1%}
⏰ **Khung thời gian:** {recommendation.time_horizon}
⚠️ **Mức rủi ro:** {recommendation.risk_level}
📈 **Tâm lý thị trường:** {recommendation.market_sentiment}

🎯 **Tín hiệu kỹ thuật:**
"""
            
            if 'error' not in signals:
                overall = signals.get('OVERALL', 'NEUTRAL')
                message += f"• Tổng thể: {overall}\n"
                
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        message += f"• {emoji} {indicator}: {signal}\n"
            
            if 'error' not in risk_report:
                message += f"""
⚠️ **Chỉ số rủi ro:**
• Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}
• Max Drawdown: {risk_report['max_drawdown']:.2%}
• Total Return: {risk_report['total_return']:.2f}%
• VaR (95%): {risk_report['var_95']:.2%}
"""
            
            # Add AI reasoning
            if recommendation.reasoning:
                message += "\n🧠 **Lý do AI đưa ra khuyến nghị:**\n"
                for i, reason in enumerate(recommendation.reasoning[:5], 1):  # Show top 5 reasons
                    message += f"• {reason}\n"
            
            # Add investment strategy
            message += f"""
📋 **Chiến lược đầu tư:**
• **Hành động:** {strategy['action']}
• **Kích thước vị thế:** {strategy['position_size']}
• **Vào lệnh:** {strategy['entry_strategy']}
• **Thoát lệnh:** {strategy['exit_strategy']}
• **Quản lý rủi ro:** {strategy['risk_management']}
"""
            
            if recommendation.target_price and recommendation.stop_loss:
                message += f"""
💰 **Mục tiêu giá:** {recommendation.target_price:,.0f} VND
🛑 **Stop Loss:** {recommendation.stop_loss:,.0f} VND
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    async def analyze_vn_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze Vietnam stock - Legacy method"""
        try:
            # Get data
            data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # Build message
            message = f"""
📊 **Phân tích {symbol} (Thị trường VN)**

💰 **Giá hiện tại:** {current_price:,.0f} VND
📈 **Thay đổi:** {change:+.2f}%

🎯 **Tín hiệu giao dịch:**
"""
            
            if 'error' not in signals:
                overall = signals.get('OVERALL', 'NEUTRAL')
                message += f"• Tổng thể: {overall}\n"
                
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        message += f"• {emoji} {indicator}: {signal}\n"
            
            if 'error' not in risk_report:
                message += f"""
⚠️ **Phân tích rủi ro:**
• Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}
• Max Drawdown: {risk_report['max_drawdown']:.2%}
• Total Return: {risk_report['total_return']:.2f}%
• VaR (95%): {risk_report['var_95']:.2%}
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    async def analyze_us_stock_with_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze US stock with AI advisor"""
        try:
            # Get data
            data = self.us_collector.get_stock_data(symbol, period="6mo")
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # AI recommendation
            recommendation = self.ai_advisor.generate_recommendation(
                symbol, data, signals, risk_report, "US"
            )
            
            # Investment strategy
            strategy = self.ai_advisor.get_investment_strategy(recommendation)
            
            # Build AI message
            message = f"""
🤖 **AI Investment Advisor - {symbol} (US)**

💰 **Giá hiện tại:** ${current_price:.2f}
📈 **Thay đổi:** {change:+.2f}%

🎯 **Khuyến nghị AI:** {recommendation.recommendation}
📊 **Độ tin cậy:** {recommendation.confidence:.1%}
⏰ **Khung thời gian:** {recommendation.time_horizon}
⚠️ **Mức rủi ro:** {recommendation.risk_level}
📈 **Tâm lý thị trường:** {recommendation.market_sentiment}

🎯 **Tín hiệu kỹ thuật:**
"""
            
            if 'error' not in signals:
                overall = signals.get('OVERALL', 'NEUTRAL')
                message += f"• Tổng thể: {overall}\n"
                
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        message += f"• {emoji} {indicator}: {signal}\n"
            
            if 'error' not in risk_report:
                message += f"""
⚠️ **Chỉ số rủi ro:**
• Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}
• Max Drawdown: {risk_report['max_drawdown']:.2%}
• Total Return: {risk_report['total_return']:.2f}%
• VaR (95%): {risk_report['var_95']:.2%}
"""
            
            # Add AI reasoning
            if recommendation.reasoning:
                message += "\n🧠 **Lý do AI đưa ra khuyến nghị:**\n"
                for i, reason in enumerate(recommendation.reasoning[:5], 1):  # Show top 5 reasons
                    message += f"• {reason}\n"
            
            # Add investment strategy
            message += f"""
📋 **Chiến lược đầu tư:**
• **Hành động:** {strategy['action']}
• **Kích thước vị thế:** {strategy['position_size']}
• **Vào lệnh:** {strategy['entry_strategy']}
• **Thoát lệnh:** {strategy['exit_strategy']}
• **Quản lý rủi ro:** {strategy['risk_management']}
"""
            
            if recommendation.target_price and recommendation.stop_loss:
                message += f"""
💰 **Mục tiêu giá:** ${recommendation.target_price:.2f}
🛑 **Stop Loss:** ${recommendation.stop_loss:.2f}
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    async def analyze_us_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze US stock - Legacy method"""
        try:
            # Get data
            data = self.us_collector.get_stock_data(symbol, period="6mo")
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # Build message
            message = f"""
📊 **Phân tích {symbol} (Thị trường Mỹ)**

💰 **Giá hiện tại:** ${current_price:.2f}
📈 **Thay đổi:** {change:+.2f}%

🎯 **Tín hiệu giao dịch:**
"""
            
            if 'error' not in signals:
                overall = signals.get('OVERALL', 'NEUTRAL')
                message += f"• Tổng thể: {overall}\n"
                
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        message += f"• {emoji} {indicator}: {signal}\n"
            
            if 'error' not in risk_report:
                message += f"""
⚠️ **Phân tích rủi ro:**
• Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}
• Max Drawdown: {risk_report['max_drawdown']:.2%}
• Total Return: {risk_report['total_return']:.2f}%
• VaR (95%): {risk_report['var_95']:.2%}
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    async def optimize_portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbols: List[str]):
        """Optimize portfolio"""
        await update.message.reply_text(f"📊 Đang tối ưu hóa portfolio: {', '.join(symbols)}...")
        
        try:
            returns_data = {}
            
            for symbol in symbols:
                # Try VN market first
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="1y")
                if data.empty:
                    # Try US market
                    data = self.us_collector.get_stock_data(symbol, period="1y")
                
                if not data.empty:
                    returns_data[symbol] = self.risk_manager.calculate_returns(data['Close'])
            
            if len(returns_data) > 1:
                import pandas as pd
                returns_df = pd.DataFrame(returns_data)
                portfolio = self.risk_manager.optimize_portfolio(returns_df, 'sharpe')
                
                message = f"""
📊 **Tối ưu hóa Portfolio**

📈 **Kết quả:**
• Expected Return: {portfolio['portfolio_return']:.2%}
• Volatility: {portfolio['portfolio_volatility']:.2%}
• Sharpe Ratio: {portfolio['sharpe_ratio']:.2f}

📊 **Khuyến nghị phân bổ:**
"""
                
                for asset, weight in portfolio['weights'].items():
                    message += f"• {asset}: {weight:.1%}\n"
                
                await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ Không đủ dữ liệu để tối ưu hóa portfolio")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tối ưu hóa portfolio: {str(e)}")
    
    async def analyze_risk(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze risk for a stock"""
        await update.message.reply_text(f"⚠️ Đang phân tích rủi ro cho {symbol}...")
        
        try:
            # Try VN market first
            data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="1y")
            if data.empty:
                # Try US market
                data = self.us_collector.get_stock_data(symbol, period="1y")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            alerts = self.risk_manager.get_risk_alerts(data, symbol)
            
            if 'error' not in risk_report:
                message = f"""
⚠️ **Phân tích rủi ro {symbol}**

📊 **Chỉ số rủi ro:**
• Volatility: {risk_report['volatility_annual']:.2%}
• Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}
• Sortino Ratio: {risk_report['sortino_ratio']:.2f}
• Max Drawdown: {risk_report['max_drawdown']:.2%}
• VaR (95%): {risk_report['var_95']:.2%}
• CVaR (95%): {risk_report['cvar_95']:.2%}
• Total Return: {risk_report['total_return']:.2f}%
"""
                
                if alerts:
                    message += "\n🚨 **Cảnh báo rủi ro:**\n"
                    for alert in alerts:
                        severity_emoji = "🚨" if alert['severity'] == 'CRITICAL' else "⚠️"
                        message += f"• {severity_emoji} {alert['message']}\n"
                else:
                    message += "\n✅ Không có cảnh báo rủi ro"
                
                await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(f"❌ Lỗi khi phân tích rủi ro: {risk_report['error']}")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích rủi ro: {str(e)}")
    
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
            
            await update.message.reply_text(full_response, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi xử lý câu hỏi: {str(e)}")
    
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
    
    async def send_welcome_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message to new users"""
        user = update.effective_user
        user_id = user.id
        
        # Check if user has already been welcomed
        if user_id in self.welcomed_users:
            return
        
        welcome_message = f"""
🤖 **Chào mừng đến với FinGPT Bot!**

Xin chào {user.first_name}! Tôi là bot AI chuyên gia tư vấn đầu tư thông minh.

🧠 **AI Investment Advisor:**
• Khuyến nghị: BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL
• Độ tin cậy: 0-100% dựa trên phân tích toàn diện
• Chiến lược đầu tư: Kích thước vị thế, vào lệnh, thoát lệnh
• Quản lý rủi ro: Target price & Stop loss tự động

🤖 **GPT Assistant - Hỏi đáp thông minh:**
• `/ask <câu hỏi>` - Giải đáp mọi thắc mắc
• `/explain <chỉ báo>` - Hiểu rõ kỹ thuật
• `/tips <chủ đề>` - Gợi ý chiến lược

📊 **Tính năng chính:**
• 📈 Phân tích kỹ thuật cổ phiếu
• 🤖 AI Advisor với khuyến nghị thông minh
• ⚠️ Quản lý rủi ro portfolio
• 📊 Tối ưu hóa danh mục đầu tư
• 🇻🇳 Hỗ trợ thị trường Việt Nam

🔧 **Lệnh AI Advisor:**
`/stock <symbol>` - **Phân tích AI toàn diện**
`/vn <symbol>` - Phân tích kỹ thuật VN
`/portfolio <symbols>` - Tối ưu hóa portfolio
`/risk <symbol>` - Phân tích rủi ro

🔧 **Lệnh GPT Assistant:**
`/ask <câu hỏi>` - **Hỏi đáp AI**
`/explain <chỉ báo>` - **Giải thích kỹ thuật**
`/tips <chủ đề>` - **Lời khuyên đầu tư**

💡 **Ví dụ AI Advisor:**
`/stock VNM` - AI phân tích VNM (Khuyến nghị + Chiến lược)
`/stock TCB` - AI phân tích TCB (Khuyến nghị + Chiến lược)
`/stock HPG` - AI phân tích HPG (Khuyến nghị + Chiến lược)

💡 **Ví dụ GPT Assistant:**
`/ask RSI là gì?` - Hỏi về chỉ báo RSI
`/explain MACD` - Giải thích chỉ báo MACD
`/tips risk` - Lời khuyên quản lý rủi ro
        """
        
        keyboard = [
            [InlineKeyboardButton("🧠 AI Investment Advisor", callback_data="analyze_stock")],
            [InlineKeyboardButton("🤖 GPT Assistant", callback_data="gpt_assistant")],
            [InlineKeyboardButton("📊 Tối ưu Portfolio", callback_data="optimize_portfolio")],
            [InlineKeyboardButton("⚠️ Phân tích rủi ro", callback_data="risk_analysis")],
            [InlineKeyboardButton("🇻🇳 Thị trường VN", callback_data="vn_market")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        # Mark user as welcomed
        self.welcomed_users.add(user_id)
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all incoming messages and send welcome to new users"""
        # Send welcome message to new users
        await self.send_welcome_message(update, context)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "analyze_stock":
            await query.edit_message_text(
                "🧠 **AI Investment Advisor**\n\n"
                "**Lệnh AI toàn diện:**\n"
                "• `/stock VNM` - AI phân tích VNM (Khuyến nghị + Chiến lược)\n"
                "• `/stock AAPL` - AI phân tích Apple (Khuyến nghị + Chiến lược)\n"
                "• `/stock TCB` - AI phân tích TCB (Khuyến nghị + Chiến lược)\n\n"
                "**Lệnh phân tích thường:**\n"
                "• `/vn VNM` - Chỉ phân tích kỹ thuật VN\n"
                "• `/us AAPL` - Chỉ phân tích kỹ thuật Mỹ\n\n"
                "🤖 **AI Advisor bao gồm:**\n"
                "• Khuyến nghị: BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL\n"
                "• Độ tin cậy: 0-100%\n"
                "• Chiến lược đầu tư chi tiết\n"
                "• Target price & Stop loss",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == "optimize_portfolio":
            await query.edit_message_text(
                "📊 **Tối ưu hóa Portfolio**\n\n"
                "Sử dụng lệnh:\n"
                "• `/portfolio VNM,TCB,HPG` - Portfolio VN\n"
                "• `/portfolio AAPL,MSFT,GOOGL` - Portfolio Mỹ",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == "risk_analysis":
            await query.edit_message_text(
                "⚠️ **Phân tích rủi ro**\n\n"
                "Sử dụng lệnh:\n"
                "• `/risk VNM` - Phân tích rủi ro cổ phiếu",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == "gpt_assistant":
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
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == "vn_market":
            await query.edit_message_text(
                "🇻🇳 **Thị trường Việt Nam**\n\n"
                "Cổ phiếu phổ biến:\n"
                "• VNM (Vinamilk)\n"
                "• TCB (Techcombank)\n"
                "• HPG (Hòa Phát)\n"
                "• FPT (FPT)\n"
                "• VIC (Vingroup)\n"
                "• VHM (Vinhomes)\n"
                "• VRE (Vincom Retail)\n"
                "• MWG (Mobile World)\n\n"
                "Lệnh: `/vn VNM` hoặc `/stock VNM`",
                parse_mode=ParseMode.MARKDOWN
            )
        elif query.data == "us_market":
            await query.edit_message_text(
                "🇺🇸 **Thị trường Mỹ**\n\n"
                "⚠️ **Tạm thời không khả dụng**\n\n"
                "Thị trường Mỹ đang được bảo trì.\n"
                "Vui lòng sử dụng thị trường Việt Nam.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stock", self.stock_command))
        application.add_handler(CommandHandler("vn", self.vn_command))
        application.add_handler(CommandHandler("us", self.us_command))
        application.add_handler(CommandHandler("portfolio", self.portfolio_command))
        application.add_handler(CommandHandler("risk", self.risk_command))
        application.add_handler(CommandHandler("ask", self.ask_command))
        application.add_handler(CommandHandler("explain", self.explain_command))
        application.add_handler(CommandHandler("tips", self.tips_command))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add handler for all messages (to send welcome to new users)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_all_messages))
        
        # Start bot
        self.logger.info("🤖 FinGPT Telegram Bot đang khởi động...")
        application.run_polling()

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