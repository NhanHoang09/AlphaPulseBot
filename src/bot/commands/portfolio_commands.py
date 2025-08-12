"""
Portfolio Management Commands
Commands cho quản lý danh mục đầu tư
"""

import numpy as np
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands
from typing import List

class PortfolioCommands(BaseCommands):
    """Portfolio Management Commands"""
    
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
            
            if len(returns_data) == 1:
                # Single stock analysis
                symbol = list(returns_data.keys())[0]
                returns = returns_data[symbol]
                
                # Calculate metrics for single stock
                expected_return = returns.mean() * 252
                volatility = returns.std() * np.sqrt(252)
                sharpe_ratio = expected_return / volatility if volatility > 0 else 0
                
                message = f"""
📊 **Phân tích Portfolio - {symbol}**

📈 **Kết quả:**
• Expected Return: {expected_return:.2%}
• Volatility: {volatility:.2%}
• Sharpe Ratio: {sharpe_ratio:.2f}

📊 **Khuyến nghị:**
• {symbol}: 100.0%

💡 **Lưu ý:** Portfolio optimization cần ít nhất 2 cổ phiếu trở lên.
Ví dụ: `/portfolio VNM,TCB,HPG`
"""
                
                await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
                
            elif len(returns_data) > 1:
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
                await update.message.reply_text("❌ Không thể lấy dữ liệu cho bất kỳ cổ phiếu nào")
                
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
