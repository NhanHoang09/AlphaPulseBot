"""
Fundamental Analysis Commands
Commands cho phân tích cơ bản và chỉ số tài chính
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class FundamentalCommands(BaseCommands):
    """Fundamental Analysis Commands"""
    
    async def fundamental_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /fundamental command"""
        if not context.args:
            await update.message.reply_text(
                "📊 <b>Fundamental Analysis</b>\n\n"
                "Sử dụng: <code>/fundamental &lt;symbol&gt; [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/fundamental VNM</code> - Phân tích cơ bản VNM\n"
                "• <code>/fundamental AAPL US</code> - Phân tích cơ bản AAPL\n"
                "• <code>/fundamental TCB VN</code> - Phân tích cơ bản TCB",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        market = context.args[1].upper() if len(context.args) > 1 else "US"
        
        if market not in ["US", "VN"]:
            await update.message.reply_text("❌ Market phải là 'US' hoặc 'VN'")
            return
        
        await update.message.reply_text(f"📊 Đang phân tích cơ bản {symbol} ({market})...")
        await self.analyze_fundamental(update, context, symbol, market)
    
    async def ratios_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ratios command"""
        if not context.args:
            await update.message.reply_text(
                "📈 <b>Financial Ratios</b>\n\n"
                "Sử dụng: <code>/ratios &lt;symbol&gt; [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/ratios VNM</code> - Chỉ số tài chính VNM\n"
                "• <code>/ratios AAPL US</code> - Chỉ số tài chính AAPL",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        market = context.args[1].upper() if len(context.args) > 1 else "US"
        
        await update.message.reply_text(f"📈 Đang tính toán chỉ số tài chính {symbol}...")
        await self.show_financial_ratios(update, context, symbol, market)
    
    async def earnings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /earnings command"""
        if not context.args:
            await update.message.reply_text(
                "💰 <b>Earnings Analysis</b>\n\n"
                "Sử dụng: <code>/earnings &lt;symbol&gt; [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/earnings VNM</code> - Phân tích thu nhập VNM\n"
                "• <code>/earnings AAPL US</code> - Phân tích thu nhập AAPL",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        market = context.args[1].upper() if len(context.args) > 1 else "US"
        
        await update.message.reply_text(f"💰 Đang phân tích thu nhập {symbol}...")
        await self.analyze_earnings(update, context, symbol, market)
    
    async def analyze_fundamental(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, market: str):
        """Phân tích cơ bản toàn diện"""
        try:
            # Get fundamental data
            fundamental_data = self.fundamental_analyzer.get_fundamental_data(symbol, market)
            
            if not fundamental_data:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cơ bản cho {symbol}")
                return
            
            # Generate comprehensive report
            report = self.fundamental_analyzer.generate_fundamental_report(symbol, market)
            
            if 'error' in report:
                await update.message.reply_text(f"❌ Lỗi phân tích cơ bản: {report['error']}")
                return
            
            # Format message
            currency = "VND" if market == "VN" else "$"
            
            message = f"""
📊 <b>Fundamental Analysis - {symbol} ({market})</b>

🎯 <b>Khuyến nghị:</b> {report['recommendation']}
📈 <b>Điểm tổng thể:</b> {report['overall_score']:.1f}/100

💰 <b>Chỉ số định giá:</b>
"""
            
            # Valuation ratios
            valuation = report['valuation_ratios']
            if valuation.get('pe_ratio'):
                message += f"• P/E Ratio: {valuation['pe_ratio']:.2f}\n"
            if valuation.get('pb_ratio'):
                message += f"• P/B Ratio: {valuation['pb_ratio']:.2f}\n"
            if valuation.get('ps_ratio'):
                message += f"• P/S Ratio: {valuation['ps_ratio']:.2f}\n"
            if valuation.get('dividend_yield'):
                message += f"• Dividend Yield: {valuation['dividend_yield']:.2f}%\n"
            
            message += f"""
📈 <b>Chỉ số sinh lời:</b>
"""
            
            # Profitability ratios
            profitability = report['profitability_ratios']
            if profitability.get('roe'):
                message += f"• ROE: {profitability['roe']:.2f}%\n"
            if profitability.get('roa'):
                message += f"• ROA: {profitability['roa']:.2f}%\n"
            if profitability.get('profit_margin'):
                message += f"• Profit Margin: {profitability['profit_margin']:.2f}%\n"
            if profitability.get('gross_margin'):
                message += f"• Gross Margin: {profitability['gross_margin']:.2f}%\n"
            
            message += f"""
🏥 <b>Sức khỏe tài chính:</b>
"""
            
            # Financial health ratios
            health = report['financial_health_ratios']
            if health.get('debt_to_equity'):
                message += f"• Debt/Equity: {health['debt_to_equity']:.2f}\n"
            if health.get('current_ratio'):
                message += f"• Current Ratio: {health['current_ratio']:.2f}\n"
            if health.get('quick_ratio'):
                message += f"• Quick Ratio: {health['quick_ratio']:.2f}\n"
            
            message += f"""
📊 <b>Chỉ số tăng trưởng:</b>
"""
            
            # Growth metrics
            growth = report['growth_metrics']
            if growth.get('revenue_growth'):
                message += f"• Revenue Growth: {growth['revenue_growth']:.2f}%\n"
            if growth.get('earnings_growth'):
                message += f"• Earnings Growth: {growth['earnings_growth']:.2f}%\n"
            if growth.get('eps_growth'):
                message += f"• EPS Growth: {growth['eps_growth']:.2f}%\n"
            
            message += f"""
📅 <b>Ngày phân tích:</b> {report['analysis_date']}

💡 <b>Lệnh liên quan:</b>
• <code>/ratios {symbol}</code> - Chỉ số chi tiết
• <code>/earnings {symbol}</code> - Phân tích thu nhập
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích cơ bản {symbol}: {str(e)}")
    
    async def show_financial_ratios(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, market: str):
        """Hiển thị chỉ số tài chính chi tiết"""
        try:
            # Get fundamental data
            fundamental_data = self.fundamental_analyzer.get_fundamental_data(symbol, market)
            
            if not fundamental_data:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Calculate all ratios
            valuation_ratios = self.fundamental_analyzer.calculate_valuation_ratios(fundamental_data)
            profitability_ratios = self.fundamental_analyzer.calculate_profitability_ratios(fundamental_data)
            financial_health_ratios = self.fundamental_analyzer.calculate_financial_health_ratios(fundamental_data)
            growth_metrics = self.fundamental_analyzer.calculate_growth_metrics(fundamental_data)
            
            # Format detailed message
            message = f"""
📈 <b>Financial Ratios - {symbol} ({market})</b>

💰 <b>Valuation Ratios:</b>
"""
            
            for key, value in valuation_ratios.items():
                if value is not None:
                    if key == 'market_cap' and value:
                        # Format market cap
                        if value >= 1e12:
                            formatted_value = f"{value/1e12:.2f}T"
                        elif value >= 1e9:
                            formatted_value = f"{value/1e9:.2f}B"
                        elif value >= 1e6:
                            formatted_value = f"{value/1e6:.2f}M"
                        else:
                            formatted_value = f"{value:,.0f}"
                        message += f"• {key.replace('_', ' ').title()}: {formatted_value}\n"
                    else:
                        message += f"• {key.replace('_', ' ').title()}: {value:.2f}\n"
            
            message += f"""
📊 <b>Profitability Ratios:</b>
"""
            
            for key, value in profitability_ratios.items():
                if value is not None:
                    message += f"• {key.replace('_', ' ').title()}: {value:.2f}%\n"
            
            message += f"""
🏥 <b>Financial Health Ratios:</b>
"""
            
            for key, value in financial_health_ratios.items():
                if value is not None:
                    message += f"• {key.replace('_', ' ').title()}: {value:.2f}\n"
            
            message += f"""
📈 <b>Growth Metrics:</b>
"""
            
            for key, value in growth_metrics.items():
                if value is not None:
                    message += f"• {key.replace('_', ' ').title()}: {value:.2f}%\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/fundamental {symbol}</code> - Phân tích cơ bản
• <code>/earnings {symbol}</code> - Phân tích thu nhập
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi hiển thị chỉ số tài chính {symbol}: {str(e)}")
    
    async def analyze_earnings(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, market: str):
        """Phân tích thu nhập"""
        try:
            # Get fundamental data
            fundamental_data = self.fundamental_analyzer.get_fundamental_data(symbol, market)
            
            if not fundamental_data:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            info = fundamental_data.get('info', {})
            financials = fundamental_data.get('financials', pd.DataFrame())
            
            # Format earnings analysis
            currency = "VND" if market == "VN" else "$"
            
            message = f"""
💰 <b>Earnings Analysis - {symbol} ({market})</b>

📊 <b>Earnings Metrics:</b>
"""
            
            # Basic earnings info
            if info.get('trailingEps'):
                message += f"• Trailing EPS: {currency}{info['trailingEps']:.2f}\n"
            if info.get('forwardEps'):
                message += f"• Forward EPS: {currency}{info['forwardEps']:.2f}\n"
            if info.get('trailingPE'):
                message += f"• Trailing P/E: {info['trailingPE']:.2f}\n"
            if info.get('forwardPE'):
                message += f"• Forward P/E: {info['forwardPE']:.2f}\n"
            
            # Revenue and income
            if info.get('totalRevenue'):
                revenue = info['totalRevenue']
                if revenue >= 1e12:
                    formatted_revenue = f"{revenue/1e12:.2f}T"
                elif revenue >= 1e9:
                    formatted_revenue = f"{revenue/1e9:.2f}B"
                elif revenue >= 1e6:
                    formatted_revenue = f"{revenue/1e6:.2f}M"
                else:
                    formatted_revenue = f"{revenue:,.0f}"
                message += f"• Total Revenue: {currency}{formatted_revenue}\n"
            
            if info.get('netIncomeToCommon'):
                net_income = info['netIncomeToCommon']
                if net_income >= 1e12:
                    formatted_income = f"{net_income/1e12:.2f}T"
                elif net_income >= 1e9:
                    formatted_income = f"{net_income/1e9:.2f}B"
                elif net_income >= 1e6:
                    formatted_income = f"{net_income/1e6:.2f}M"
                else:
                    formatted_income = f"{net_income:,.0f}"
                message += f"• Net Income: {currency}{formatted_income}\n"
            
            # Growth metrics
            growth_metrics = self.fundamental_analyzer.calculate_growth_metrics(fundamental_data)
            
            message += f"""
📈 <b>Growth Analysis:</b>
"""
            
            for key, value in growth_metrics.items():
                if value is not None:
                    message += f"• {key.replace('_', ' ').title()}: {value:.2f}%\n"
            
            # Cash flow
            message += f"""
💵 <b>Cash Flow:</b>
"""
            
            if info.get('operatingCashflow'):
                op_cf = info['operatingCashflow']
                if op_cf >= 1e12:
                    formatted_op_cf = f"{op_cf/1e12:.2f}T"
                elif op_cf >= 1e9:
                    formatted_op_cf = f"{op_cf/1e9:.2f}B"
                elif op_cf >= 1e6:
                    formatted_op_cf = f"{op_cf/1e6:.2f}M"
                else:
                    formatted_op_cf = f"{op_cf:,.0f}"
                message += f"• Operating Cash Flow: {currency}{formatted_op_cf}\n"
            
            if info.get('freeCashflow'):
                fcf = info['freeCashflow']
                if fcf >= 1e12:
                    formatted_fcf = f"{fcf/1e12:.2f}T"
                elif fcf >= 1e9:
                    formatted_fcf = f"{fcf/1e9:.2f}B"
                elif fcf >= 1e6:
                    formatted_fcf = f"{fcf/1e6:.2f}M"
                else:
                    formatted_fcf = f"{fcf:,.0f}"
                message += f"• Free Cash Flow: {currency}{formatted_fcf}\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/fundamental {symbol}</code> - Phân tích cơ bản
• <code>/ratios {symbol}</code> - Chỉ số tài chính
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích thu nhập {symbol}: {str(e)}")
