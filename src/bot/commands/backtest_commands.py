"""
Backtesting Commands
Commands cho backtesting chiến lược giao dịch
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class BacktestCommands(BaseCommands):
    """Backtesting Commands"""
    
    async def backtest_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /backtest command"""
        if not context.args:
            await update.message.reply_text(
                "📊 <b>Strategy Backtesting</b>\n\n"
                "Sử dụng: <code>/backtest &lt;symbol&gt; &lt;strategy&gt; [capital]</code>\n"
                "Ví dụ:\n"
                "• <code>/backtest VNM moving_average</code> - Backtest MA strategy\n"
                "• <code>/backtest AAPL rsi 10000</code> - Backtest RSI với $10k\n"
                "• <code>/backtest TCB bollinger</code> - Backtest Bollinger strategy",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        strategy = context.args[1].lower() if len(context.args) > 1 else 'moving_average'
        initial_capital = float(context.args[2]) if len(context.args) > 2 else 10000
        
        await update.message.reply_text(f"📊 Đang backtest {strategy} strategy cho {symbol}...")
        await self.run_backtest(update, context, symbol, strategy, initial_capital)
    
    async def strategy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /strategy command"""
        if not context.args:
            await update.message.reply_text(
                "🎯 <b>Strategy Analysis</b>\n\n"
                "Sử dụng: <code>/strategy &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/strategy VNM</code> - Phân tích chiến lược cho VNM\n"
                "• <code>/strategy AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "6mo"
        
        await update.message.reply_text(f"🎯 Đang phân tích chiến lược cho {symbol}...")
        await self.analyze_strategy(update, context, symbol, period)
    
    async def performance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /performance command"""
        if not context.args:
            await update.message.reply_text(
                "📈 <b>Performance Analysis</b>\n\n"
                "Sử dụng: <code>/performance &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/performance VNM</code> - Phân tích hiệu suất VNM\n"
                "• <code>/performance AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "1y"
        
        await update.message.reply_text(f"📈 Đang phân tích hiệu suất {symbol}...")
        await self.analyze_performance(update, context, symbol, period)
    
    async def run_backtest(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                          symbol: str, strategy: str, initial_capital: float):
        """Chạy backtest cho một chiến lược"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="1y")
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period="1y")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Run backtest
            result = self.backtester.backtest_strategy(data, strategy, initial_capital)
            
            if 'error' in result:
                await update.message.reply_text(f"❌ Lỗi backtest: {result['error']}")
                return
            
            # Generate report
            report = self.backtester.generate_backtest_report(result)
            
            # Format message
            message = f"""
📊 <b>Backtest Report - {symbol}</b>

🎯 <b>Strategy:</b> {result['strategy'].replace('_', ' ').title()}
💰 <b>Initial Capital:</b> ${result['initial_capital']:,.0f}
💵 <b>Final Capital:</b> ${result['final_capital']:,.0f}

📈 <b>Performance:</b>
• Total Return: {result['total_return']:.2%}
• Annualized Return: {result['annualized_return']:.2%}
• Sharpe Ratio: {result['sharpe_ratio']:.2f}
• Max Drawdown: {result['max_drawdown']:.2%}

🎯 <b>Trading Statistics:</b>
• Total Trades: {result['total_trades']}
• Win Rate: {result['win_rate']:.2%}
• Winning Trades: {result['winning_trades']}
• Losing Trades: {result['losing_trades']}

📅 <b>Date:</b> {result['backtest_date']}

💡 <b>Lệnh liên quan:</b>
• <code>/strategy {symbol}</code> - Phân tích chiến lược
• <code>/performance {symbol}</code> - Phân tích hiệu suất
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi backtest {symbol}: {str(e)}")
    
    async def analyze_strategy(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                              symbol: str, period: str):
        """Phân tích chiến lược giao dịch"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Add technical indicators
            data_with_indicators = self.analyzer.add_all_indicators(data)
            
            # Analyze different strategies
            strategies = {
                'moving_average': self._analyze_ma_strategy(data_with_indicators),
                'rsi': self._analyze_rsi_strategy(data_with_indicators),
                'bollinger': self._analyze_bollinger_strategy(data_with_indicators),
                'macd': self._analyze_macd_strategy(data_with_indicators)
            }
            
            # Format message
            message = f"""
🎯 <b>Strategy Analysis - {symbol}</b>

📊 <b>Period:</b> {period}
📅 <b>Data Points:</b> {len(data):,}
💰 <b>Current Price:</b> ${data['Close'].iloc[-1]:.2f}

📈 <b>Strategy Performance:</b>
"""
            
            for strategy_name, performance in strategies.items():
                if performance:
                    message += f"""
• <b>{strategy_name.replace('_', ' ').title()}:</b>
  - Signal: {performance['signal']}
  - Confidence: {performance['confidence']:.1%}
  - Expected Return: {performance['expected_return']:.2%}
"""
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/backtest {symbol} moving_average</code> - Backtest MA strategy
• <code>/performance {symbol}</code> - Phân tích hiệu suất
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích chiến lược {symbol}: {str(e)}")
    
    async def analyze_performance(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                 symbol: str, period: str):
        """Phân tích hiệu suất"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Calculate performance metrics
            returns = data['Close'].pct_change().dropna()
            
            # Basic metrics
            total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1
            annualized_return = (1 + total_return) ** (252 / len(data)) - 1
            volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
            
            # Risk metrics
            max_drawdown = self._calculate_max_drawdown(data['Close'])
            var_95 = returns.quantile(0.05)
            
            # Format message
            message = f"""
📈 <b>Performance Analysis - {symbol}</b>

📊 <b>Period:</b> {period}
📅 <b>Data Points:</b> {len(data):,}
💰 <b>Current Price:</b> ${data['Close'].iloc[-1]:.2f}

📈 <b>Return Metrics:</b>
• Total Return: {total_return:.2%}
• Annualized Return: {annualized_return:.2%}
• Volatility: {volatility:.2%}
• Sharpe Ratio: {sharpe_ratio:.2f}

⚠️ <b>Risk Metrics:</b>
• Max Drawdown: {max_drawdown:.2%}
• VaR (95%): {var_95:.2%}
• Beta: {self._calculate_beta(returns):.2f}

📊 <b>Price Statistics:</b>
• Highest Price: ${data['High'].max():.2f}
• Lowest Price: ${data['Low'].min():.2f}
• Average Price: ${data['Close'].mean():.2f}
• Price Range: ${data['High'].max() - data['Low'].min():.2f}

💡 <b>Lệnh liên quan:</b>
• <code>/backtest {symbol} moving_average</code> - Backtest strategy
• <code>/strategy {symbol}</code> - Phân tích chiến lược
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích hiệu suất {symbol}: {str(e)}")
    
    def _analyze_ma_strategy(self, data: pd.DataFrame) -> Dict:
        """Phân tích Moving Average strategy"""
        try:
            if len(data) < 50:
                return {}
            
            latest = data.iloc[-1]
            
            # Check MA crossover
            if latest['SMA_20'] > latest['SMA_50']:
                signal = "BUY"
                confidence = 0.7
                expected_return = 0.05
            elif latest['SMA_20'] < latest['SMA_50']:
                signal = "SELL"
                confidence = 0.7
                expected_return = -0.03
            else:
                signal = "HOLD"
                confidence = 0.5
                expected_return = 0.0
            
            return {
                'signal': signal,
                'confidence': confidence,
                'expected_return': expected_return
            }
            
        except Exception as e:
            return {}
    
    def _analyze_rsi_strategy(self, data: pd.DataFrame) -> Dict:
        """Phân tích RSI strategy"""
        try:
            if len(data) < 14:
                return {}
            
            latest = data.iloc[-1]
            rsi = latest.get('RSI', 50)
            
            if rsi < 30:
                signal = "BUY"
                confidence = 0.8
                expected_return = 0.08
            elif rsi > 70:
                signal = "SELL"
                confidence = 0.8
                expected_return = -0.05
            else:
                signal = "HOLD"
                confidence = 0.6
                expected_return = 0.02
            
            return {
                'signal': signal,
                'confidence': confidence,
                'expected_return': expected_return
            }
            
        except Exception as e:
            return {}
    
    def _analyze_bollinger_strategy(self, data: pd.DataFrame) -> Dict:
        """Phân tích Bollinger Bands strategy"""
        try:
            if len(data) < 20:
                return {}
            
            latest = data.iloc[-1]
            close = latest['Close']
            bb_upper = latest.get('BB_Upper', close)
            bb_lower = latest.get('BB_Lower', close)
            
            if close <= bb_lower:
                signal = "BUY"
                confidence = 0.75
                expected_return = 0.06
            elif close >= bb_upper:
                signal = "SELL"
                confidence = 0.75
                expected_return = -0.04
            else:
                signal = "HOLD"
                confidence = 0.5
                expected_return = 0.01
            
            return {
                'signal': signal,
                'confidence': confidence,
                'expected_return': expected_return
            }
            
        except Exception as e:
            return {}
    
    def _analyze_macd_strategy(self, data: pd.DataFrame) -> Dict:
        """Phân tích MACD strategy"""
        try:
            if len(data) < 26:
                return {}
            
            latest = data.iloc[-1]
            macd = latest.get('MACD', 0)
            macd_signal = latest.get('MACD_Signal', 0)
            
            if macd > macd_signal:
                signal = "BUY"
                confidence = 0.7
                expected_return = 0.04
            elif macd < macd_signal:
                signal = "SELL"
                confidence = 0.7
                expected_return = -0.03
            else:
                signal = "HOLD"
                confidence = 0.5
                expected_return = 0.0
            
            return {
                'signal': signal,
                'confidence': confidence,
                'expected_return': expected_return
            }
            
        except Exception as e:
            return {}
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Tính toán max drawdown"""
        try:
            cumulative = (1 + prices.pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return drawdown.min()
        except Exception as e:
            return 0.0
    
    def _calculate_beta(self, returns: pd.Series) -> float:
        """Tính toán beta (simplified)"""
        try:
            # Simplified beta calculation
            # In real implementation, this would compare to market returns
            return 1.0  # Placeholder
        except Exception as e:
            return 1.0
