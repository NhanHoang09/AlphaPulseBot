"""
AI Investment Advisor Commands
Commands cho phân tích AI toàn diện
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class AICommands(BaseCommands):
    """AI Investment Advisor Commands"""
    
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
    
    async def analyze_stock_with_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Analyze stock with AI advisor (VN market only)"""
        await update.message.reply_text(f"🤖 Đang phân tích {symbol} với AI Advisor...")
        
        # Try VN market only
        data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
        if not data.empty:
            await self.analyze_vn_stock_with_ai(update, context, symbol)
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
            
            # Use common analysis logic
            await self._analyze_stock_with_ai_common(update, context, symbol, data, "VN")
            
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
            
            # Use the same analysis logic as VN but with US market
            await self._analyze_stock_with_ai_common(update, context, symbol, data, "US")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    async def _analyze_stock_with_ai_common(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, data, market: str):
        """Common AI analysis logic for both VN and US markets"""
        current_price = data['Close'].iloc[-1]
        change = data['Returns'].iloc[-1] * 100
        
        # Technical analysis
        data_with_indicators = self.analyzer.add_all_indicators(data)
        signals = self.analyzer.get_trading_signals(data_with_indicators)
        
        # Risk analysis
        risk_report = self.risk_manager.generate_risk_report(data, symbol)
        
        # AI recommendation
        recommendation = self.ai_advisor.generate_recommendation(
            symbol, data, signals, risk_report, market
        )
        
        # Investment strategy
        strategy = self.ai_advisor.get_investment_strategy(recommendation)
        
        # Build AI message
        currency = "VND" if market == "VN" else "$"
        price_format = f"{current_price:,.0f}" if market == "VN" else f"{current_price:.2f}"
        
        message = f"""
🤖 **AI Investment Advisor - {symbol} ({market})**

💰 **Giá hiện tại:** {currency}{price_format}
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
            target_format = f"{recommendation.target_price:,.0f}" if market == "VN" else f"{recommendation.target_price:.2f}"
            stop_format = f"{recommendation.stop_loss:,.0f}" if market == "VN" else f"{recommendation.stop_loss:.2f}"
            message += f"""
💰 **Mục tiêu giá:** {currency}{target_format}
🛑 **Stop Loss:** {currency}{stop_format}
"""
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
