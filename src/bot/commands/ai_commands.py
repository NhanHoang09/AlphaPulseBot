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
    
    async def quick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quick command - Quick analysis for traders"""
        if not context.args:
            await update.message.reply_text(
                "⚡ <b>Quick Analysis</b>\n\n"
                "Sử dụng: <code>/quick &lt;symbol&gt;</code>\n"
                "Phân tích nhanh cho trader bận rộn\n"
                "Ví dụ: <code>/quick VNM</code>, <code>/quick AAPL</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        await self.quick_analysis(update, context, symbol)
    
    async def scan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /scan command - Alias for /quick"""
        if not context.args:
            await update.message.reply_text(
                "🔍 <b>Stock Scanner</b>\n\n"
                "Sử dụng: <code>/scan &lt;symbol&gt;</code>\n"
                "Quick scan cho trader chuyên nghiệp\n"
                "Ví dụ: <code>/scan VNM</code>, <code>/scan AAPL</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        await self.quick_analysis(update, context, symbol)
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command - Alias for /stock"""
        if not context.args:
            await update.message.reply_text(
                "🔍 <b>Stock Checker</b>\n\n"
                "Sử dụng: <code>/check &lt;symbol&gt;</code>\n"
                "Deep analysis cho trader chuyên nghiệp\n"
                "Ví dụ: <code>/check VNM</code>, <code>/check AAPL</code>",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        await self.analyze_stock_with_ai(update, context, symbol)
    
    async def quick_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
        """Quick analysis for busy traders"""
        await update.message.reply_text(f"⚡ Đang phân tích nhanh {symbol}...")
        
        try:
            # Determine market
            if symbol.endswith('.VN') or len(symbol) <= 3:
                market = "VN"
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
            else:
                market = "US"
                data = self.us_collector.get_stock_data(symbol, period="6mo")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Quick technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Quick fundamental analysis
            fundamental_data = self.fundamental_analyzer.get_fundamental_data(symbol, market)
            valuation_ratios = {}
            if fundamental_data:
                valuation_ratios = self.fundamental_analyzer.calculate_valuation_ratios(fundamental_data)
            
            # Quick risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # Current price and change
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100 if 'Returns' in data.columns else 0
            
            # Format quick message
            currency = "VND" if market == "VN" else "$"
            price_format = f"{current_price:,.0f}" if market == "VN" else f"{current_price:.2f}"
            
            message = f"""
⚡ <b>Quick Analysis - {symbol} ({market})</b>

💰 <b>Price:</b> {currency}{price_format} ({change:+.2f}%)

🎯 <b>Technical Signals:</b>
"""
            
            if 'error' not in signals:
                overall = signals.get('OVERALL', 'NEUTRAL')
                emoji = "🟢" if "BUY" in overall else "🔴" if "SELL" in overall else "🟡"
                message += f"• Overall: {emoji} {overall}\n"
                
                # Show key signals
                key_signals = ['RSI', 'MACD', 'MA']
                for signal in key_signals:
                    if signal in signals:
                        signal_value = signals[signal]
                        emoji = "🟢" if "BUY" in signal_value else "🔴" if "SELL" in signal_value else "🟡"
                        message += f"• {signal}: {emoji} {signal_value}\n"
            
            message += f"""
💰 <b>Valuation:</b>
"""
            
            if valuation_ratios:
                if valuation_ratios.get('pe_ratio'):
                    pe = valuation_ratios['pe_ratio']
                    pe_status = "🟢" if pe and pe < 15 else "🔴" if pe and pe > 25 else "🟡"
                    message += f"• P/E: {pe_status} {pe:.2f}\n"
                
                if valuation_ratios.get('pb_ratio'):
                    pb = valuation_ratios['pb_ratio']
                    pb_status = "🟢" if pb and pb < 1.5 else "🔴" if pb and pb > 3 else "🟡"
                    message += f"• P/B: {pb_status} {pb:.2f}\n"
                
                if valuation_ratios.get('dividend_yield'):
                    div_yield = valuation_ratios['dividend_yield']
                    div_status = "🟢" if div_yield and div_yield > 3 else "🟡"
                    message += f"• Dividend: {div_status} {div_yield:.2f}%\n"
            
            message += f"""
⚠️ <b>Risk:</b>
"""
            
            if 'error' not in risk_report:
                sharpe = risk_report.get('sharpe_ratio', 0)
                sharpe_status = "🟢" if sharpe > 1 else "🔴" if sharpe < 0 else "🟡"
                message += f"• Sharpe: {sharpe_status} {sharpe:.2f}\n"
                
                max_dd = risk_report.get('max_drawdown', 0)
                dd_status = "🟢" if max_dd > -0.1 else "🔴" if max_dd < -0.2 else "🟡"
                message += f"• Max DD: {dd_status} {max_dd:.1%}\n"
                
                volatility = risk_report.get('volatility_annual', 0)
                vol_status = "🟢" if volatility < 0.2 else "🔴" if volatility > 0.4 else "🟡"
                message += f"• Volatility: {vol_status} {volatility:.1%}\n"
            
            message += f"""
💡 <b>Quick Decision:</b>
"""
            
            # Simple decision logic
            buy_signals = 0
            sell_signals = 0
            
            if 'error' not in signals:
                for signal in signals.values():
                    if 'BUY' in signal:
                        buy_signals += 1
                    elif 'SELL' in signal:
                        sell_signals += 1
            
            if buy_signals > sell_signals:
                message += "🟢 <b>BULLISH</b> - Có thể mua\n"
            elif sell_signals > buy_signals:
                message += "🔴 <b>BEARISH</b> - Có thể bán\n"
            else:
                message += "🟡 <b>NEUTRAL</b> - Chờ tín hiệu rõ ràng\n"
            
            message += f"""
📋 <b>Next Steps:</b>
• <code>/stock {symbol}</code> - Phân tích chi tiết
• <code>/fundamental {symbol}</code> - Cơ bản
• <code>/risk {symbol}</code> - Rủi ro
• <code>/predict {symbol}</code> - Dự báo
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích nhanh {symbol}: {str(e)}")
    
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
