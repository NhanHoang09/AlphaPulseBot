"""
Market Sentiment Commands
Commands cho phân tích sentiment thị trường
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class SentimentCommands(BaseCommands):
    """Market Sentiment Commands"""
    
    async def sentiment_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sentiment command"""
        if not context.args:
            await update.message.reply_text(
                "📊 <b>Market Sentiment Analysis</b>\n\n"
                "Sử dụng: <code>/sentiment &lt;symbol&gt; [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/sentiment VNM</code> - Sentiment VNM\n"
                "• <code>/sentiment AAPL US</code> - Sentiment AAPL\n"
                "• <code>/sentiment market US</code> - Sentiment thị trường Mỹ",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        market = context.args[1].upper() if len(context.args) > 1 else "US"
        
        if market not in ["US", "VN"]:
            await update.message.reply_text("❌ Market phải là 'US' hoặc 'VN'")
            return
        
        await update.message.reply_text(f"📊 Đang phân tích sentiment {symbol} ({market})...")
        await self.analyze_sentiment(update, context, symbol, market)
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /news command"""
        if not context.args:
            await update.message.reply_text(
                "📰 <b>News Sentiment Analysis</b>\n\n"
                "Sử dụng: <code>/news &lt;symbol&gt; [days]</code>\n"
                "Ví dụ:\n"
                "• <code>/news VNM</code> - Tin tức 7 ngày qua\n"
                "• <code>/news AAPL 3</code> - Tin tức 3 ngày qua",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        days = int(context.args[1]) if len(context.args) > 1 else 7
        
        await update.message.reply_text(f"📰 Đang phân tích tin tức {symbol} ({days} ngày)...")
        await self.analyze_news_sentiment(update, context, symbol, days)
    
    async def market_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /market command"""
        if not context.args:
            await update.message.reply_text(
                "🌍 <b>Market Overview</b>\n\n"
                "Sử dụng: <code>/market [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/market</code> - Tổng quan thị trường Mỹ\n"
                "• <code>/market VN</code> - Tổng quan thị trường VN",
                parse_mode=ParseMode.HTML
            )
            return
        
        market = context.args[0].upper() if context.args else "US"
        
        if market not in ["US", "VN"]:
            await update.message.reply_text("❌ Market phải là 'US' hoặc 'VN'")
            return
        
        await update.message.reply_text(f"🌍 Đang phân tích thị trường {market}...")
        await self.show_market_overview(update, context, market)
    
    async def sector_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sector command"""
        if not context.args:
            await update.message.reply_text(
                "🏭 <b>Sector Rotation Analysis</b>\n\n"
                "Sử dụng: <code>/sector [market]</code>\n"
                "Ví dụ:\n"
                "• <code>/sector</code> - Sector rotation Mỹ\n"
                "• <code>/sector VN</code> - Sector rotation VN",
                parse_mode=ParseMode.HTML
            )
            return
        
        market = context.args[0].upper() if context.args else "US"
        
        if market not in ["US", "VN"]:
            await update.message.reply_text("❌ Market phải là 'US' hoặc 'VN'")
            return
        
        await update.message.reply_text(f"🏭 Đang phân tích sector rotation {market}...")
        await self.show_sector_rotation(update, context, market)
    
    async def analyze_sentiment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, market: str):
        """Phân tích sentiment toàn diện"""
        try:
            # Generate comprehensive sentiment report
            report = self.sentiment_analyzer.generate_market_sentiment_report(symbol, market)
            
            if 'error' in report:
                await update.message.reply_text(f"❌ Lỗi phân tích sentiment: {report['error']}")
                return
            
            # Format message
            message = f"""
📊 <b>Market Sentiment Analysis - {symbol} ({market})</b>

🎯 <b>Sentiment tổng thể:</b> {report['overall_sentiment'].replace('_', ' ').title()}
📅 <b>Ngày phân tích:</b> {report['analysis_date']}
"""
            
            # News sentiment
            if 'news_sentiment' in report and 'error' not in report['news_sentiment']:
                news = report['news_sentiment']
                message += f"""
📰 <b>News Sentiment:</b>
• Sentiment: {news['sentiment_label'].replace('_', ' ').title()}
• Số bài báo: {news['articles_count']}
• Score: {news['overall_sentiment']:.3f}
"""
            
            # Market breadth
            if 'market_breadth' in report and 'error' not in report['market_breadth']:
                breadth = report['market_breadth']
                message += f"""
📈 <b>Market Breadth:</b>
• Advancing: {breadth['advancing']}
• Declining: {breadth['declining']}
• A/D Ratio: {breadth['advance_decline_ratio']:.2f}
• New Highs: {breadth['new_highs']}
• New Lows: {breadth['new_lows']}
"""
            
            # Economic indicators
            if 'economic_indicators' in report and 'error' not in report['economic_indicators']:
                econ = report['economic_indicators']
                message += f"""
💹 <b>Economic Indicators:</b>
• VIX: {econ['vix']:.1f}
• USD Index: {econ['usd_index']:.1f}
• Gold: ${econ['gold_price']:.0f}
• Oil: ${econ['oil_price']:.1f}
• 10Y Yield: {econ['bond_yield_10y']:.2f}%
• Fed Rate: {econ['fed_rate']:.2f}%
"""
            
            # Social sentiment
            if 'social_sentiment' in report and 'error' not in report['social_sentiment']:
                social = report['social_sentiment']
                message += f"""
📱 <b>Social Sentiment:</b>
• Overall: {social['sentiment_label'].replace('_', ' ').title()}
• Score: {social['overall_social_sentiment']:.3f}
• Volume: {social['social_volume']:,}
"""
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/news {symbol}</code> - Phân tích tin tức
• <code>/market {market}</code> - Tổng quan thị trường
• <code>/sector {market}</code> - Sector rotation
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích sentiment {symbol}: {str(e)}")
    
    async def analyze_news_sentiment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, days: int):
        """Phân tích sentiment tin tức"""
        try:
            # Get news sentiment
            news_sentiment = self.sentiment_analyzer.get_news_sentiment(symbol, days)
            
            if 'error' in news_sentiment:
                await update.message.reply_text(f"❌ Lỗi phân tích tin tức: {news_sentiment['error']}")
                return
            
            # Format message
            message = f"""
📰 <b>News Sentiment Analysis - {symbol}</b>

📊 <b>Thống kê:</b>
• Số bài báo: {news_sentiment['articles_count']}
• Sentiment: {news_sentiment['sentiment_label'].replace('_', ' ').title()}
• Score: {news_sentiment['overall_sentiment']:.3f}
• Thời gian: {days} ngày qua
"""
            
            # Show recent articles
            if news_sentiment.get('articles'):
                message += f"""
📰 <b>Bài báo gần đây:</b>
"""
                
                for i, article in enumerate(news_sentiment['articles'][:3], 1):
                    title = article.get('title', 'No title')[:100]
                    source = article.get('source', {}).get('name', 'Unknown')
                    published = article.get('publishedAt', '')[:10]
                    
                    message += f"""
{i}. <b>{title}</b>
   📰 {source} | 📅 {published}
"""
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/sentiment {symbol}</code> - Sentiment toàn diện
• <code>/market</code> - Tổng quan thị trường
• <code>/stock {symbol}</code> - Phân tích AI toàn diện
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phân tích tin tức {symbol}: {str(e)}")
    
    async def show_market_overview(self, update: Update, context: ContextTypes.DEFAULT_TYPE, market: str):
        """Hiển thị tổng quan thị trường"""
        try:
            # Get market data
            market_breadth = self.sentiment_analyzer.get_market_breadth(market)
            economic_indicators = self.sentiment_analyzer.get_economic_indicators()
            sector_rotation = self.sentiment_analyzer.get_sector_rotation(market)
            
            # Format message
            message = f"""
🌍 <b>Market Overview - {market}</b>

📈 <b>Market Breadth:</b>
"""
            
            if 'error' not in market_breadth:
                breadth = market_breadth
                message += f"""
• Advancing: {breadth['advancing']}
• Declining: {breadth['declining']}
• Unchanged: {breadth['unchanged']}
• A/D Ratio: {breadth['advance_decline_ratio']:.2f}
• New Highs: {breadth['new_highs']}
• New Lows: {breadth['new_lows']}
"""
            
            message += f"""
💹 <b>Economic Indicators:</b>
"""
            
            if 'error' not in economic_indicators:
                econ = economic_indicators
                message += f"""
• VIX: {econ['vix']:.1f} {'🟢' if econ['vix'] < 20 else '🟡' if econ['vix'] < 30 else '🔴'}
• USD Index: {econ['usd_index']:.1f}
• Gold: ${econ['gold_price']:.0f}
• Oil: ${econ['oil_price']:.1f}
• 10Y Yield: {econ['bond_yield_10y']:.2f}%
• Fed Rate: {econ['fed_rate']:.2f}%
• Inflation: {econ['inflation_rate']:.1f}%
• Unemployment: {econ['unemployment_rate']:.1f}%
"""
            
            message += f"""
🏭 <b>Sector Rotation:</b>
"""
            
            if 'error' not in sector_rotation:
                rotation = sector_rotation
                message += f"""
• Direction: {rotation['rotation_direction'].replace('_', ' ').title()}
• Avg Performance: {rotation['average_performance']:.2%}

<b>Top Performing Sectors:</b>
"""
                
                for sector, data in rotation['top_performing_sectors']:
                    emoji = "🟢" if data['momentum'] == 'bullish' else "🔴" if data['momentum'] == 'bearish' else "🟡"
                    message += f"• {emoji} {sector}: {data['performance']:.2%}\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/sector {market}</code> - Sector rotation chi tiết
• <code>/sentiment market {market}</code> - Sentiment thị trường
• <code>/portfolio</code> - Tối ưu portfolio
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi hiển thị tổng quan thị trường {market}: {str(e)}")
    
    async def show_sector_rotation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, market: str):
        """Hiển thị sector rotation"""
        try:
            # Get sector rotation data
            sector_data = self.sentiment_analyzer.get_sector_rotation(market)
            
            if 'error' in sector_data:
                await update.message.reply_text(f"❌ Lỗi sector rotation: {sector_data['error']}")
                return
            
            # Format message
            message = f"""
🏭 <b>Sector Rotation Analysis - {market}</b>

📊 <b>Tổng quan:</b>
• Direction: {sector_data['rotation_direction'].replace('_', ' ').title()}
• Average Performance: {sector_data['average_performance']:.2%}

📈 <b>Tất cả Sectors:</b>
"""
            
            # Sort sectors by performance
            sorted_sectors = sorted(sector_data['sectors'].items(), 
                                  key=lambda x: x[1]['performance'], 
                                  reverse=True)
            
            for sector, data in sorted_sectors:
                emoji = "🟢" if data['momentum'] == 'bullish' else "🔴" if data['momentum'] == 'bearish' else "🟡"
                performance = data['performance']
                momentum = data['momentum'].replace('_', ' ').title()
                
                message += f"• {emoji} {sector}: {performance:.2%} ({momentum})\n"
            
            message += f"""
💡 <b>Lệnh liên quan:</b>
• <code>/market {market}</code> - Tổng quan thị trường
• <code>/sentiment market {market}</code> - Sentiment thị trường
• <code>/portfolio</code> - Tối ưu portfolio
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi hiển thị sector rotation {market}: {str(e)}")
