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
        
        if query.data == "core_services":
            await self.show_core_services_menu(query)
        elif query.data == "analysis_module":
            await self.show_analysis_module_menu(query)
        elif query.data == "portfolio_risk":
            await self.show_portfolio_risk_menu(query)
        elif query.data == "ai_tools":
            await self.show_ai_tools_menu(query)
        elif query.data == "model_management":
            await self.show_model_management_menu(query)
        elif query.data == "back_to_main":
            await self.show_main_menu(query)
        # Help command handlers
        elif query.data == "help_core":
            await self.show_help_core(query)
        elif query.data == "help_analysis":
            await self.show_help_analysis(query)
        elif query.data == "help_portfolio":
            await self.show_help_portfolio(query)
        elif query.data == "help_ai":
            await self.show_help_ai(query)
        elif query.data == "help_model":
            await self.show_help_model(query)
        elif query.data == "help_architecture":
            await self.show_help_architecture(query)
        elif query.data == "help_workflow":
            await self.show_help_workflow(query)
        elif query.data == "help_back":
            await self.show_help_back(query)
        # Legacy callback handlers for backward compatibility
        elif query.data == "quick_analysis_help":
            await self.show_help_core(query)
        elif query.data == "deep_analysis_help":
            await self.show_help_analysis(query)
        elif query.data == "portfolio_risk":
            await self.show_help_portfolio(query)
        elif query.data == "ai_tools":
            await self.show_help_ai(query)
        elif query.data == "back_to_start":
            await self.show_back_to_start(query)
    
    async def show_main_menu(self, query):
        """Show main menu"""
        user = query.from_user
        welcome_message = f"""
🤖 **AlphaPulse Trading Bot**

👋 Hello {user.first_name}! I'm your professional trading assistant.

🎯 **Tôi sẽ giúp bạn:**
• Phân tích thị trường toàn diện
• Tìm cổ phiếu tiềm năng
• Đưa ra quyết định đầu tư thông minh
• Quản lý rủi ro hiệu quả

💡 **Workflow đề xuất:** Market → Stock → Analysis → Decision → Portfolio
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Core Services", callback_data="core_services")],
            [InlineKeyboardButton("🔍 Analysis Module", callback_data="analysis_module")],
            [InlineKeyboardButton("📊 Portfolio & Strategy", callback_data="portfolio_risk")],
            [InlineKeyboardButton("🤖 AI Module", callback_data="ai_tools")],
            [InlineKeyboardButton("📋 Model Management", callback_data="model_management")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_market_overview_menu(self, query):
        """Show market overview menu"""
        keyboard = [
            [InlineKeyboardButton("📊 Market Overview", callback_data="market_overview_help")],
            [InlineKeyboardButton("🏭 Sector Rotation", callback_data="sector_rotation_help")],
            [InlineKeyboardButton("📰 Market Sentiment", callback_data="market_sentiment_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🌍 **Market Overview**\n\n"
            "**Hiểu tổng quan thị trường trước khi đầu tư**\n\n"
            "**Commands:**\n"
            "• `/market [market]` - Tổng quan thị trường\n"
            "• `/sector [market]` - Sector rotation analysis\n"
            "• `/sentiment market [market]` - Market sentiment\n\n"
            "**Ví dụ:**\n"
            "• `/market VN` - Thị trường VN\n"
            "• `/sector US` - Sector rotation Mỹ\n"
            "• `/sentiment market VN` - Sentiment VN",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_stock_analysis_menu(self, query):
        """Show stock analysis menu"""
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Analysis", callback_data="quick_analysis_help")],
            [InlineKeyboardButton("🤖 AI Analysis", callback_data="ai_analysis_help")],
            [InlineKeyboardButton("📊 Fundamental", callback_data="fundamental_help")],
            [InlineKeyboardButton("💰 Earnings", callback_data="earnings_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔍 **Stock Analysis**\n\n"
            "**Phân tích toàn diện một cổ phiếu cụ thể**\n\n"
            "**Commands:**\n"
            "• `/quick <symbol>` - Phân tích nhanh (30s)\n"
            "• `/stock <symbol>` - AI phân tích toàn diện\n"
            "• `/fundamental <symbol>` - Phân tích cơ bản\n"
            "• `/ratios <symbol>` - Chỉ số tài chính\n"
            "• `/earnings <symbol>` - Phân tích thu nhập\n\n"
            "**Ví dụ:**\n"
            "• `/quick VNM` - Phân tích nhanh VNM\n"
            "• `/stock AAPL` - AI phân tích Apple\n"
            "• `/fundamental TCB` - Cơ bản TCB",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_portfolio_risk_menu(self, query):
        """Show portfolio & risk menu"""
        keyboard = [
            [InlineKeyboardButton("📊 Portfolio Optimization", callback_data="portfolio_help")],
            [InlineKeyboardButton("⚠️ Risk Analysis", callback_data="risk_help")],
            [InlineKeyboardButton("📈 Strategy Backtesting", callback_data="backtest_help")],
            [InlineKeyboardButton("📊 Strategy Analysis", callback_data="strategy_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 **Portfolio & Strategy Management**\n\n"
            "**Quản lý danh mục và chiến lược**\n\n"
            "**Commands:**\n"
            "• `/portfolio <symbols>` - Tối ưu hóa portfolio\n"
            "• `/risk <symbol>` - Phân tích rủi ro chi tiết\n"
            "• `/backtest <symbol> <strategy>` - Strategy backtesting\n"
            "• `/strategy <symbol>` - Strategy analysis\n\n"
            "**Ví dụ:**\n"
            "• `/portfolio VNM,TCB,HPG` - Tối ưu 3 cổ phiếu\n"
            "• `/risk VNM` - Phân tích rủi ro VNM\n"
            "• `/backtest VNM moving_average` - Backtest MA strategy\n"
            "• `/strategy TCB` - Strategy analysis TCB",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_ai_tools_menu(self, query):
        """Show AI tools menu"""
        keyboard = [
            [InlineKeyboardButton("🤖 GPT Assistant", callback_data="gpt_help")],
            [InlineKeyboardButton("🧠 Claude AI", callback_data="claude_help")],
            [InlineKeyboardButton("💡 Trading Tips", callback_data="tips_help")],
            [InlineKeyboardButton("📰 News Analysis", callback_data="news_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🤖 **AI Tools**\n\n"
            "**Hỗ trợ quyết định với AI**\n\n"
            "**Commands:**\n"
            "• `/ask <question>` - GPT Assistant (Miễn phí)\n"
            "• `/claude <question>` - Claude AI (Có phí)\n"
            "• `/tips <topic>` - Lời khuyên đầu tư\n"
            "• `/news <symbol>` - Phân tích tin tức\n\n"
            "**Ví dụ:**\n"
            "• `/ask RSI là gì?` - Hỏi về RSI\n"
            "• `/claude Phân tích thị trường VN?` - Phân tích sâu\n"
            "• `/tips risk` - Lời khuyên quản lý rủi ro\n"
            "• `/news VNM` - Tin tức VNM",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_technical_analysis_menu(self, query):
        """Show technical analysis menu"""
        keyboard = [
            [InlineKeyboardButton("📈 Basic Technical", callback_data="basic_technical_help")],
            [InlineKeyboardButton("🔮 AI Prediction", callback_data="prediction_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📈 **Technical Analysis**\n\n"
            "**Xác định điểm vào/ra và timing**\n\n"
            "**Commands:**\n"
            "• `/explain <indicator>` - Giải thích chỉ báo\n"
            "• `/predict <symbol>` - Dự báo giá với AI\n\n"
            "**Ví dụ:**\n"
            "• `/explain RSI` - Giải thích RSI\n"
            "• `/explain MACD` - Giải thích MACD\n"
            "• `/predict VNM` - Dự báo VNM\n"
            "• `/predict AAPL lstm` - Dự báo với LSTM",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_advanced_analysis_menu(self, query):
        """Show advanced analysis menu"""
        keyboard = [
            [InlineKeyboardButton("📐 Fibonacci", callback_data="fibonacci_help")],
            [InlineKeyboardButton("🌊 Elliott Wave", callback_data="elliott_help")],
            [InlineKeyboardButton("📊 Volume Profile", callback_data="volume_help")],
            [InlineKeyboardButton("☁️ Ichimoku", callback_data="ichimoku_help")],
            [InlineKeyboardButton("📈 Options", callback_data="options_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📐 **Advanced Technical Analysis**\n\n"
            "**Phân tích kỹ thuật nâng cao cho trader chuyên nghiệp**\n\n"
            "**Commands:**\n"
            "• `/fibonacci <symbol>` - Fibonacci retracements\n"
            "• `/elliott <symbol>` - Elliott Wave analysis\n"
            "• `/volume <symbol>` - Volume Profile analysis\n"
            "• `/ichimoku <symbol>` - Ichimoku Cloud\n"
            "• `/options <symbol>` - Options analysis\n\n"
            "**Ví dụ:**\n"
            "• `/fibonacci VNM` - Fibonacci VNM\n"
            "• `/elliott AAPL` - Elliott Wave AAPL\n"
            "• `/volume TCB` - Volume Profile TCB\n"
            "• `/ichimoku MSFT` - Ichimoku MSFT\n"
            "• `/options TSLA` - Options TSLA",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_backtesting_menu(self, query):
        """Show backtesting menu"""
        keyboard = [
            [InlineKeyboardButton("📊 Strategy Backtesting", callback_data="backtest_help")],
            [InlineKeyboardButton("📈 Strategy Analysis", callback_data="strategy_help")],
            [InlineKeyboardButton("📊 Performance Analysis", callback_data="performance_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 **Backtesting & Strategy**\n\n"
            "**Kiểm tra hiệu quả chiến lược giao dịch**\n\n"
            "**Commands:**\n"
            "• `/backtest <symbol> <strategy>` - Backtest chiến lược\n"
            "• `/strategy <symbol>` - Phân tích chiến lược\n"
            "• `/performance <symbol>` - Phân tích hiệu suất\n\n"
            "**Ví dụ:**\n"
            "• `/backtest VNM moving_average` - Backtest MA strategy\n"
            "• `/backtest AAPL rsi 10000` - Backtest RSI với $10k\n"
            "• `/strategy TCB` - Phân tích chiến lược TCB\n"
            "• `/performance VNM` - Hiệu suất VNM",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_model_management_menu(self, query):
        """Show model management menu"""
        keyboard = [
            [InlineKeyboardButton("🤖 Train Models", callback_data="train_help")],
            [InlineKeyboardButton("📋 Model Status", callback_data="model_status_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📋 **Model Management**\n\n"
            "**Training và quản lý AI models**\n\n"
            "**Commands:**\n"
            "• `/train <symbol> [model]` - Training AI model\n"
            "• `/model_status <symbol>` - Kiểm tra model\n"
            "• `/predict <symbol> [model]` - Dự báo với model\n\n"
            "**Ví dụ:**\n"
            "• `/train VNM lstm` - Training LSTM cho VNM\n"
            "• `/train VNM ensemble` - Training Ensemble\n"
            "• `/model_status VNM` - Kiểm tra model VNM\n"
            "• `/predict VNM lstm` - Dự báo với LSTM",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_quick_decisions_menu(self, query):
        """Show quick decisions menu"""
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Analysis", callback_data="quick_analysis_help")],
            [InlineKeyboardButton("🤖 AI Analysis", callback_data="ai_analysis_help")],
            [InlineKeyboardButton("⚠️ Risk Analysis", callback_data="risk_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚡ **Quick Decisions**\n\n"
            "**Commands sử dụng nhiều nhất - 80% thời gian trading**\n\n"
            "**Commands:**\n"
            "• `/quick <symbol>` - Phân tích nhanh (30s) - MOST USED\n"
            "• `/stock <symbol>` - AI phân tích toàn diện (2 phút)\n"
            "• `/risk <symbol>` - Phân tích rủi ro nhanh\n\n"
            "**Ví dụ:**\n"
            "• `/quick VNM` - Quick scan VNM\n"
            "• `/stock AAPL` - Deep analysis Apple\n"
            "• `/risk TCB` - Risk check TCB\n\n"
            "**💡 Tip:** Sử dụng `/quick` cho 80% quyết định trading",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_deep_analysis_menu(self, query):
        """Show deep analysis menu"""
        keyboard = [
            [InlineKeyboardButton("📊 Fundamental", callback_data="fundamental_help")],
            [InlineKeyboardButton("💰 Financial Ratios", callback_data="ratios_help")],
            [InlineKeyboardButton("📈 Earnings", callback_data="earnings_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔍 **Deep Analysis**\n\n"
            "**Commands cho nghiên cứu chi tiết - 15% thời gian**\n\n"
            "**Commands:**\n"
            "• `/fundamental <symbol>` - Phân tích cơ bản\n"
            "• `/ratios <symbol>` - Chỉ số tài chính chi tiết\n"
            "• `/earnings <symbol>` - Phân tích thu nhập\n\n"
            "**Ví dụ:**\n"
            "• `/fundamental VNM` - Fundamental VNM\n"
            "• `/ratios AAPL US` - Ratios Apple\n"
            "• `/earnings TCB` - Earnings TCB\n\n"
            "**💡 Tip:** Dùng cho cổ phiếu quan trọng hoặc nghiên cứu sâu",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_core_services_menu(self, query):
        """Show core services menu"""
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Analysis", callback_data="quick_analysis_help")],
            [InlineKeyboardButton("🤖 AI Analysis", callback_data="ai_analysis_help")],
            [InlineKeyboardButton("⚠️ Risk Analysis", callback_data="risk_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚡ **Core Services**\n\n"
            "**Commands sử dụng nhiều nhất - 80% thời gian trading**\n\n"
            "**Commands:**\n"
            "• `/quick <symbol>` - Phân tích nhanh (30s) - MOST USED\n"
            "• `/stock <symbol>` - AI phân tích toàn diện (2 phút)\n"
            "• `/risk <symbol>` - Phân tích rủi ro nhanh\n\n"
            "**Aliases:**\n"
            "• `/scan <symbol>` - Alias cho `/quick`\n"
            "• `/check <symbol>` - Alias cho `/stock`\n\n"
            "**Ví dụ:**\n"
            "• `/scan VNM` - Quick scan VNM\n"
            "• `/check AAPL` - Deep analysis Apple\n"
            "• `/risk TCB` - Risk check TCB\n\n"
            "**💡 Tip:** Sử dụng `/scan` cho 80% quyết định trading",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_analysis_module_menu(self, query):
        """Show analysis module menu"""
        keyboard = [
            [InlineKeyboardButton("📊 Fundamental", callback_data="fundamental_help")],
            [InlineKeyboardButton("📈 Technical", callback_data="technical_help")],
            [InlineKeyboardButton("📐 Advanced", callback_data="advanced_help")],
            [InlineKeyboardButton("📰 Sentiment", callback_data="sentiment_help")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔍 **Analysis Module**\n\n"
            "**Commands cho nghiên cứu chi tiết - 15% thời gian**\n\n"
            "**📊 Fundamental Analysis:**\n"
            "• `/fundamental <symbol>` - Phân tích cơ bản\n"
            "• `/ratios <symbol>` - Chỉ số tài chính\n"
            "• `/earnings <symbol>` - Phân tích thu nhập\n\n"
            "**📈 Technical Analysis:**\n"
            "• `/explain <indicator>` - Giải thích chỉ báo kỹ thuật\n"
            "• `/predict <symbol> [model]` - Dự báo giá với AI\n\n"
            "**📐 Advanced Technical:**\n"
            "• `/fibonacci <symbol> [period]` - Fibonacci Analysis\n"
            "• `/elliott <symbol> [period]` - Elliott Wave Analysis\n"
            "• `/volume <symbol> [period]` - Volume Profile Analysis\n"
            "• `/ichimoku <symbol> [period]` - Ichimoku Cloud Analysis\n"
            "• `/options <symbol> [expiry]` - Options Analysis\n\n"
            "**📰 Sentiment Analysis:**\n"
            "• `/sentiment <symbol> [market]` - Market sentiment\n"
            "• `/news <symbol> [days]` - Phân tích tin tức\n"
            "• `/market [market]` - Tổng quan thị trường\n"
            "• `/sector [market]` - Sector rotation analysis",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    # Help command methods
    async def show_help_core(self, query):
        """Show core services help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
⚡ **CORE SERVICES (Dịch vụ cốt lõi)**
**Commands sử dụng nhiều nhất - 80% thời gian trading**

• `/quick <symbol>` - **Phân tích nhanh (30s) - MOST USED**
  - Technical + Valuation + Risk summary
  - Quick decision cho trader bận rộn
  - Ví dụ: `/quick VNM`, `/quick AAPL`
  - **Alias:** `/scan <symbol>` - Stock scanner

• `/stock <symbol>` - **AI phân tích toàn diện (2 phút)**
  - AI recommendation + Technical + Fundamental + Risk
  - Target price, Stop loss, Strategy
  - Ví dụ: `/stock VNM`, `/stock AAPL`
  - **Alias:** `/check <symbol>` - Stock checker

• `/risk <symbol>` - **Phân tích rủi ro nhanh**
  - VaR, Max drawdown, Volatility
  - Risk alerts, Risk assessment
  - Ví dụ: `/risk VNM`, `/risk TCB`

**💡 Tip:** Sử dụng `/scan` cho 80% quyết định trading
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_analysis(self, query):
        """Show analysis module help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🔍 **ANALYSIS MODULE (Phân tích)**
**Commands cho nghiên cứu chi tiết - 15% thời gian**

**📊 Fundamental Analysis:**
• `/fundamental <symbol> [market]` - Phân tích cơ bản
• `/ratios <symbol> [market]` - Chỉ số tài chính chi tiết
• `/earnings <symbol> [market]` - Phân tích thu nhập

**📈 Technical Analysis:**
• `/explain <indicator>` - Giải thích chỉ báo kỹ thuật
• `/predict <symbol> [model]` - Dự báo giá với AI

**📐 Advanced Technical:**
• `/fibonacci <symbol> [period]` - Fibonacci Analysis
• `/elliott <symbol> [period]` - Elliott Wave Analysis
• `/volume <symbol> [period]` - Volume Profile Analysis
• `/ichimoku <symbol> [period]` - Ichimoku Cloud Analysis
• `/options <symbol> [expiry]` - Options Analysis

**📰 Sentiment Analysis:**
• `/sentiment <symbol> [market]` - Market sentiment
• `/news <symbol> [days]` - Phân tích tin tức
• `/market [market]` - Tổng quan thị trường
• `/sector [market]` - Sector rotation analysis
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_portfolio(self, query):
        """Show portfolio & strategy help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
📊 **PORTFOLIO & STRATEGY MODULE**
**Quản lý danh mục và chiến lược**

• `/portfolio <symbols>` - **Tối ưu hóa portfolio**
  - Modern Portfolio Theory
  - Optimal weights, Sharpe ratio
  - Ví dụ: `/portfolio VNM,TCB,HPG`

• `/backtest <symbol> <strategy> [capital]` - **Strategy Backtesting**
  - Moving Average strategy, RSI strategy
  - Bollinger Bands strategy, Performance metrics
  - Ví dụ: `/backtest VNM moving_average`

• `/strategy <symbol> [period]` - **Strategy Analysis**
  - Multiple strategy comparison, Signal analysis
  - Expected returns calculation
  - Ví dụ: `/strategy VNM`

• `/performance <symbol> [period]` - **Performance Analysis**
  - Return metrics, Risk metrics, Price statistics
  - Ví dụ: `/performance VNM`
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_ai(self, query):
        """Show AI module help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🤖 **AI MODULE (Trí tuệ nhân tạo)**
**Hỗ trợ quyết định với AI**

• `/ask <question>` - **GPT Assistant (Miễn phí)**
  - Hỏi đáp tài chính, Trading tips
  - Ví dụ: `/ask RSI là gì?`

• `/claude <question>` - **Claude AI (Có phí)**
  - Phân tích chuyên sâu, Market insights
  - Ví dụ: `/claude Phân tích xu hướng thị trường VN?`

• `/tips <topic>` - **Lời khuyên đầu tư**
  - Topics: `general`, `technical`, `risk`
  - Ví dụ: `/tips general`
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_model(self, query):
        """Show model management help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
📋 **MODEL MANAGEMENT MODULE**
**Training và quản lý AI models**

• `/train <symbol> [model]` - **Training AI model**
  - LSTM, Ensemble models
  - Ví dụ: `/train VNM lstm`

• `/model_status <symbol> [model]` - **Kiểm tra model**
  - Model performance, Status
  - Ví dụ: `/model_status VNM`
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_architecture(self, query):
        """Show architecture help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🏗️ **KIẾN TRÚC MODULE**

**📁 Core Services:**
- `TradingService` - Business logic chính
- `MarketService` - Market data & context
- `ConfigurationService` - Cấu hình hệ thống

**📁 Analysis Module:**
- `TechnicalAnalyzer` - Phân tích kỹ thuật
- `FundamentalAnalyzer` - Phân tích cơ bản
- `SentimentAnalyzer` - Phân tích sentiment
- `AdvancedTechnicalAnalyzer` - Phân tích nâng cao
- `OptionsAnalyzer` - Phân tích options
- `Backtester` - Backtesting strategies

**📁 AI Module:**
- `AIInvestmentAdvisor` - AI advisor chính
- `GPTAssistant` - GPT assistant
- `ClaudeAssistant` - Claude AI
- `FinGPTModel` - Custom FinGPT model

**📁 Bot Module:**
- `CommandFactory` - Command management
- Modular commands theo chức năng
- Button handlers cho UI

**🎯 Tổng cộng: 29 Commands**
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_workflow(self, query):
        """Show workflow tips help"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Help", callback_data="help_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
💡 **WORKFLOW TRADING CHUYÊN NGHIỆP**

**🔄 Daily Trading Workflow:**

**Morning Session (9:00-10:00):**
```bash
/scan VNM          # Quick scan watchlist
/scan TCB          # Quick scan watchlist
/market VN          # Market context
```

**Analysis Session (10:00-11:00):**
```bash
/check VNM         # Deep analysis
/risk VNM          # Risk check
/fundamental VNM   # Fundamental check
```

**Execution Session (11:00-12:00):**
```bash
/predict VNM       # Price prediction
/fibonacci VNM     # Entry/exit levels
/portfolio VNM,TCB,HPG  # Portfolio check
```

**⚡ Speed Trading Tips:**
1. **Sử dụng `/scan` cho 80% quyết định**
2. **Dùng `/check` cho cổ phiếu quan trọng**
3. **Luôn check `/risk` trước khi mua**
4. **Hỏi AI khi không chắc**

**🎯 Priority Commands:**
- **MOST USED:** `/scan`, `/check`, `/risk`
- **DAILY:** `/market`, `/predict`
- **WEEKLY:** `/portfolio`, `/strategy`
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_help_back(self, query):
        """Show main help menu"""
        keyboard = [
            [InlineKeyboardButton("⚡ Core Services", callback_data="help_core")],
            [InlineKeyboardButton("🔍 Analysis Module", callback_data="help_analysis")],
            [InlineKeyboardButton("📊 Portfolio & Strategy", callback_data="help_portfolio")],
            [InlineKeyboardButton("🤖 AI Module", callback_data="help_ai")],
            [InlineKeyboardButton("📋 Model Management", callback_data="help_model")],
            [InlineKeyboardButton("🏗️ Architecture", callback_data="help_architecture")],
            [InlineKeyboardButton("💡 Workflow Tips", callback_data="help_workflow")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🤖 **AlphaPulse Trading Bot v2.0 - Professional Commands**

📋 **Commands được sắp xếp theo MODULE ARCHITECTURE**

**Chọn phần bạn muốn xem chi tiết:**

⚡ **Core Services** - Commands chính (80% usage)
🔍 **Analysis Module** - Tất cả phân tích (15% usage)  
📊 **Portfolio & Strategy** - Quản lý danh mục
🤖 **AI Module** - AI assistants
📋 **Model Management** - Quản lý AI models
🏗️ **Architecture** - Kiến trúc hệ thống
💡 **Workflow Tips** - Tips cho trader

**💡 Quick Start:**
• `/scan <symbol>` - Quick analysis (alias: `/quick`)
• `/check <symbol>` - Deep analysis (alias: `/stock`)
• `/risk <symbol>` - Risk analysis

**📊 Popular Stocks:**
🇻🇳 VNM, TCB, HPG, FPT | 🇺🇸 AAPL, MSFT, GOOGL, TSLA
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_quick_analysis_help(self, query):
        """Show quick analysis help"""
        keyboard = [
            [InlineKeyboardButton("🔍 Try /scan VNM", callback_data="try_scan")],
            [InlineKeyboardButton("📊 Try /scan AAPL", callback_data="try_scan_aapl")],
            [InlineKeyboardButton("⬅️ Back to Start", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
⚡ **QUICK ANALYSIS (30 giây)**

**Commands chính cho trader bận rộn:**

• `/scan <symbol>` - **Stock Scanner (MOST USED)**
  - Technical + Valuation + Risk summary
  - Quick decision cho trader bận rộn
  - **Alias:** `/quick <symbol>`

**Ví dụ:**
• `/scan VNM` - Quick scan VNM
• `/scan AAPL` - Quick scan Apple
• `/scan TCB` - Quick scan TCB

**💡 Khi nào dùng:**
- 80% thời gian trading
- Cần quyết định nhanh
- Scan watchlist hàng ngày
- Market opening/closing

**📊 Kết quả bao gồm:**
- Technical indicators (RSI, MACD, MA)
- Valuation metrics (P/E, P/B)
- Risk assessment (VaR, Volatility)
- Quick recommendation
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_deep_analysis_help(self, query):
        """Show deep analysis help"""
        keyboard = [
            [InlineKeyboardButton("🔍 Try /check VNM", callback_data="try_check")],
            [InlineKeyboardButton("📊 Try /check AAPL", callback_data="try_check_aapl")],
            [InlineKeyboardButton("⬅️ Back to Start", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🔍 **DEEP ANALYSIS (2 phút)**

**Commands cho nghiên cứu chi tiết:**

• `/check <symbol>` - **AI Deep Analysis**
  - AI recommendation + Technical + Fundamental + Risk
  - Target price, Stop loss, Strategy
  - **Alias:** `/stock <symbol>`

**Ví dụ:**
• `/check VNM` - Deep analysis VNM
• `/check AAPL` - Deep analysis Apple
• `/check TCB` - Deep analysis TCB

**💡 Khi nào dùng:**
- 15% thời gian trading
- Cổ phiếu quan trọng
- Trước khi mua bán lớn
- Weekly analysis

**📊 Kết quả bao gồm:**
- AI recommendation với confidence level
- Technical analysis chi tiết
- Fundamental analysis
- Risk metrics đầy đủ
- Target price & Stop loss
- Investment strategy
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def show_back_to_start(self, query):
        """Show back to start menu"""
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Analysis", callback_data="quick_analysis_help")],
            [InlineKeyboardButton("🔍 Deep Analysis", callback_data="deep_analysis_help")],
            [InlineKeyboardButton("📊 Portfolio & Risk", callback_data="portfolio_risk")],
            [InlineKeyboardButton("🤖 AI Tools", callback_data="ai_tools")],
            [InlineKeyboardButton("📋 All Commands", callback_data="help_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        help_text = """
🤖 **AlphaPulse Trading Bot v2.0**

💡 **Quick Start Commands:**
• `/scan <symbol>` - Quick analysis (30s)
• `/check <symbol>` - Deep analysis (2 phút)
• `/risk <symbol>` - Risk analysis

📊 **Popular Stocks:**
🇻🇳 VNM, TCB, HPG, FPT | 🇺🇸 AAPL, MSFT, GOOGL, TSLA

📋 **Xem tất cả commands:** `/help`
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
