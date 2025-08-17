"""
Advanced Technical Commands
Commands cho phân tích kỹ thuật nâng cao
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class AdvancedCommands(BaseCommands):
    """Advanced Technical Commands"""
    
    async def fibonacci_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /fibonacci command"""
        if not context.args:
            await update.message.reply_text(
                "📐 <b>Fibonacci Analysis</b>\n\n"
                "Sử dụng: <code>/fibonacci &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/fibonacci VNM</code> - Phân tích Fibonacci VNM\n"
                "• <code>/fibonacci AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "6mo"
        
        await update.message.reply_text(f"📐 Đang phân tích Fibonacci {symbol}...")
        await self.analyze_fibonacci(update, context, symbol, period)
    
    async def elliott_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /elliott command"""
        if not context.args:
            await update.message.reply_text(
                "🌊 <b>Elliott Wave Analysis</b>\n\n"
                "Sử dụng: <code>/elliott &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/elliott VNM</code> - Phân tích Elliott Wave VNM\n"
                "• <code>/elliott AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "6mo"
        
        await update.message.reply_text(f"🌊 Đang phân tích Elliott Wave {symbol}...")
        await self.analyze_elliott_wave(update, context, symbol, period)
    
    async def volume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /volume command"""
        if not context.args:
            await update.message.reply_text(
                "📊 <b>Volume Profile Analysis</b>\n\n"
                "Sử dụng: <code>/volume &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/volume VNM</code> - Phân tích Volume Profile VNM\n"
                "• <code>/volume AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "6mo"
        
        await update.message.reply_text(f"📊 Đang phân tích Volume Profile {symbol}...")
        await self.analyze_volume_profile(update, context, symbol, period)
    
    async def ichimoku_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ichimoku command"""
        if not context.args:
            await update.message.reply_text(
                "☁️ <b>Ichimoku Cloud Analysis</b>\n\n"
                "Sử dụng: <code>/ichimoku &lt;symbol&gt; [period]</code>\n"
                "Ví dụ:\n"
                "• <code>/ichimoku VNM</code> - Phân tích Ichimoku VNM\n"
                "• <code>/ichimoku AAPL 1y</code> - Phân tích 1 năm",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        period = context.args[1] if len(context.args) > 1 else "6mo"
        
        await update.message.reply_text(f"☁️ Đang phân tích Ichimoku Cloud {symbol}...")
        await self.analyze_ichimoku(update, context, symbol, period)
    
    async def options_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /options command"""
        if not context.args:
            await update.message.reply_text(
                "📈 <b>Options Analysis</b>\n\n"
                "Sử dụng: <code>/options &lt;symbol&gt; [expiry]</code>\n"
                "Ví dụ:\n"
                "• <code>/options AAPL</code> - Phân tích options AAPL\n"
                "• <code>/options TSLA 2024-02-16</code> - Phân tích expiry cụ thể",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        expiry = context.args[1] if len(context.args) > 1 else None
        
        await update.message.reply_text(f"📈 Đang phân tích options {symbol}...")
        await self.analyze_options(update, context, symbol, expiry)
    
    async def analyze_fibonacci(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                               symbol: str, period: str):
        """Phân tích Fibonacci"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Find swing points
            swing_points = self.advanced_analyzer.find_swing_points(data)
            
            if not swing_points:
                await update.message.reply_text(f"❌ Không tìm thấy swing points cho {symbol}")
                return
            
            # Calculate Fibonacci levels
            fib_analysis = self.advanced_analyzer.calculate_fibonacci_retracements(
                data,
                swing_points['current_swing_high'],
                swing_points['current_swing_low']
            )
            
            if not fib_analysis:
                await update.message.reply_text(f"❌ Lỗi tính toán Fibonacci cho {symbol}")
                return
            
            # Format message
            current_price = data['Close'].iloc[-1]
            currency = "VND" if symbol.endswith('.VN') or len(symbol) <= 3 else "$"
            
            message = f"""
📐 <b>Fibonacci Analysis - {symbol}</b>

📊 <b>Swing Points:</b>
• Swing High: {currency}{swing_points['current_swing_high']:,.2f}
• Swing Low: {currency}{swing_points['current_swing_low']:,.2f}
• Current Price: {currency}{current_price:,.2f}

📐 <b>Fibonacci Levels:</b>
"""
            
            # Show key Fibonacci levels
            levels = fib_analysis['levels']
            key_levels = ['fib_0', 'fib_236', 'fib_382', 'fib_500', 'fib_618', 'fib_786', 'fib_1000']
            
            for level in key_levels:
                if level in levels:
                    price = levels[level]
                    distance = abs(current_price - price) / price * 100
                    emoji = "🎯" if distance < 2 else "📊"
                    message += f"• {emoji} {level.replace('fib_', '')}%: {currency}{price:,.2f} ({distance:.1f}% away)\n"
            
            # Support/Resistance analysis
            message += f"""
🎯 <b>Support/Resistance:</b>
"""
            
            # Find nearest support and resistance
            supports = [levels['fib_382'], levels['fib_500'], levels['fib_618']]
            resistances = [levels['fib_236'], levels['fib_0']]
            
            nearest_support = min(supports, key=lambda x: abs(x - current_price))
            nearest_resistance = min(resistances, key=lambda x: abs(x - current_price))
            
            support_distance = (current_price - nearest_support) / current_price * 100
            resistance_distance = (nearest_resistance - current_price) / current_price * 100
            
            message += f"• Nearest Support: {currency}{nearest_support:,.2f} ({support_distance:.1f}% below)\n"
            message += f"• Nearest Resistance: {currency}{nearest_resistance:,.2f} ({resistance_distance:.1f}% above)\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/elliott {symbol}</code> - Elliott Wave analysis
• <code>/volume {symbol}</code> - Volume Profile analysis
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích Fibonacci {symbol}: {str(e)}")
    
    async def analyze_elliott_wave(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                  symbol: str, period: str):
        """Phân tích Elliott Wave"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Detect Elliott Wave pattern
            elliott_analysis = self.advanced_analyzer.detect_elliott_wave_pattern(data)
            
            if 'error' in elliott_analysis:
                await update.message.reply_text(f"❌ Lỗi Elliott Wave: {elliott_analysis['error']}")
                return
            
            # Format message
            current_price = data['Close'].iloc[-1]
            currency = "VND" if symbol.endswith('.VN') or len(symbol) <= 3 else "$"
            
            message = f"""
🌊 <b>Elliott Wave Analysis - {symbol}</b>

📊 <b>Pattern Detection:</b>
• Pattern Type: {elliott_analysis['pattern']}
• Wave Count: {elliott_analysis['wave_count']}
• Current Wave: {elliott_analysis['current_wave']}
• Trend Direction: {elliott_analysis['trend_direction']}
• Confidence: {elliott_analysis['confidence']:.1%}

💰 <b>Current Price:</b> {currency}{current_price:,.2f}

📈 <b>Wave Characteristics:</b>
"""
            
            if elliott_analysis['pattern'] == 'Impulse Wave (Uptrend)':
                message += """
• Wave 1: Initial move up
• Wave 2: Retracement (usually 50-78.6%)
• Wave 3: Strongest move (often 1.618x Wave 1)
• Wave 4: Consolidation
• Wave 5: Final push (often weaker than Wave 3)
"""
            elif elliott_analysis['pattern'] == 'Impulse Wave (Downtrend)':
                message += """
• Wave 1: Initial move down
• Wave 2: Retracement (usually 50-78.6%)
• Wave 3: Strongest move (often 1.618x Wave 1)
• Wave 4: Consolidation
• Wave 5: Final push (often weaker than Wave 3)
"""
            else:
                message += """
• Wave A: Initial correction
• Wave B: Retracement (usually 50-78.6% of Wave A)
• Wave C: Final correction (often equal to Wave A)
"""
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/fibonacci {symbol}</code> - Fibonacci analysis
• <code>/volume {symbol}</code> - Volume Profile analysis
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích Elliott Wave {symbol}: {str(e)}")
    
    async def analyze_volume_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                    symbol: str, period: str):
        """Phân tích Volume Profile"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Calculate Volume Profile
            volume_profile = self.advanced_analyzer.calculate_volume_profile(data)
            
            if 'error' in volume_profile:
                await update.message.reply_text(f"❌ Lỗi Volume Profile: {volume_profile['error']}")
                return
            
            # Format message
            current_price = data['Close'].iloc[-1]
            currency = "VND" if symbol.endswith('.VN') or len(symbol) <= 3 else "$"
            
            message = f"""
📊 <b>Volume Profile Analysis - {symbol}</b>

💰 <b>Current Price:</b> {currency}{current_price:,.2f}

🎯 <b>Key Levels:</b>
• POC (Point of Control): {currency}{volume_profile['poc_price']:,.2f}
• Value Area High: {currency}{volume_profile['value_area_high']:,.2f}
• Value Area Low: {currency}{volume_profile['value_area_low']:,.2f}

📈 <b>Volume Analysis:</b>
• Total Volume: {volume_profile['total_volume']:,.0f}
• POC Volume: {volume_profile['poc_volume']:,.0f}
• Value Area: 70% of total volume

📊 <b>Price Position:</b>
"""
            
            # Analyze current price position
            poc_price = volume_profile['poc_price']
            value_high = volume_profile['value_area_high']
            value_low = volume_profile['value_area_low']
            
            if current_price > value_high:
                position = "Above Value Area (Overvalued)"
                sentiment = "Bearish"
            elif current_price < value_low:
                position = "Below Value Area (Undervalued)"
                sentiment = "Bullish"
            elif current_price > poc_price:
                position = "Above POC (Slightly Overvalued)"
                sentiment = "Neutral to Bearish"
            else:
                position = "Below POC (Slightly Undervalued)"
                sentiment = "Neutral to Bullish"
            
            message += f"• Position: {position}\n"
            message += f"• Sentiment: {sentiment}\n"
            
            # Distance to key levels
            poc_distance = abs(current_price - poc_price) / current_price * 100
            message += f"• Distance to POC: {poc_distance:.1f}%\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/fibonacci {symbol}</code> - Fibonacci analysis
• <code>/elliott {symbol}</code> - Elliott Wave analysis
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích Volume Profile {symbol}: {str(e)}")
    
    async def analyze_ichimoku(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                              symbol: str, period: str):
        """Phân tích Ichimoku Cloud"""
        try:
            # Get market data
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period=period)
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Calculate Ichimoku Cloud
            ichimoku_data = self.advanced_analyzer.calculate_ichimoku_cloud(data)
            
            if ichimoku_data.empty:
                await update.message.reply_text(f"❌ Lỗi tính toán Ichimoku cho {symbol}")
                return
            
            # Get latest values
            latest = ichimoku_data.iloc[-1]
            current_price = latest['Close']
            currency = "VND" if symbol.endswith('.VN') or len(symbol) <= 3 else "$"
            
            # Analyze signals
            tenkan = latest.get('tenkan_sen', current_price)
            kijun = latest.get('kijun_sen', current_price)
            senkou_a = latest.get('senkou_span_a', current_price)
            senkou_b = latest.get('senkou_span_b', current_price)
            chikou = latest.get('chikou_span', current_price)
            
            # Determine signals
            signals = []
            
            # Tenkan/Kijun crossover
            if tenkan > kijun:
                signals.append("🟢 Tenkan > Kijun (Bullish)")
            else:
                signals.append("🔴 Tenkan < Kijun (Bearish)")
            
            # Price vs Cloud
            cloud_high = max(senkou_a, senkou_b)
            cloud_low = min(senkou_a, senkou_b)
            
            if current_price > cloud_high:
                signals.append("🟢 Price above Cloud (Bullish)")
            elif current_price < cloud_low:
                signals.append("🔴 Price below Cloud (Bearish)")
            else:
                signals.append("🟡 Price inside Cloud (Neutral)")
            
            # Cloud color
            if senkou_a > senkou_b:
                signals.append("🟢 Cloud is Green (Bullish)")
            else:
                signals.append("🔴 Cloud is Red (Bearish)")
            
            # Format message
            message = f"""
☁️ <b>Ichimoku Cloud Analysis - {symbol}</b>

💰 <b>Current Price:</b> {currency}{current_price:,.2f}

📊 <b>Ichimoku Levels:</b>
• Tenkan-sen: {currency}{tenkan:,.2f}
• Kijun-sen: {currency}{kijun:,.2f}
• Senkou Span A: {currency}{senkou_a:,.2f}
• Senkou Span B: {currency}{senkou_b:,.2f}
• Chikou Span: {currency}{chikou:,.2f}

🎯 <b>Cloud Analysis:</b>
• Cloud High: {currency}{cloud_high:,.2f}
• Cloud Low: {currency}{cloud_low:,.2f}
• Cloud Thickness: {currency}{cloud_high - cloud_low:,.2f}

📈 <b>Signals:</b>
"""
            
            for signal in signals:
                message += f"• {signal}\n"
            
            # Overall sentiment
            bullish_count = sum(1 for s in signals if "🟢" in s)
            bearish_count = sum(1 for s in signals if "🔴" in s)
            
            if bullish_count > bearish_count:
                overall_sentiment = "Bullish"
            elif bearish_count > bullish_count:
                overall_sentiment = "Bearish"
            else:
                overall_sentiment = "Neutral"
            
            message += f"""
🎯 <b>Overall Sentiment:</b> {overall_sentiment}

💡 <b>Lệnh liên quan:</b>
• <code>/fibonacci {symbol}</code> - Fibonacci analysis
• <code>/elliott {symbol}</code> - Elliott Wave analysis
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích Ichimoku {symbol}: {str(e)}")
    
    async def analyze_options(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                             symbol: str, expiry: str = None):
        """Phân tích Options"""
        try:
            # Placeholder implementation
            # In real implementation, this would fetch options data
            
            message = f"""
📈 <b>Options Analysis - {symbol}</b>

⚠️ <b>Note:</b> Options analysis requires real-time options data.
This feature is currently in development.

📊 <b>What's Available:</b>
• Put/Call Ratio analysis
• Implied Volatility calculation
• Greeks calculation (Delta, Gamma, Theta, Vega)
• Options flow analysis
• Max Pain calculation

💡 <b>Lệnh liên quan:</b>
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
• <code>/sentiment {symbol}</code> - Market sentiment
• <code>/fundamental {symbol}</code> - Fundamental analysis
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích Options {symbol}: {str(e)}")
