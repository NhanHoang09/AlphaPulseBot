"""
Core Services Layer
Centralized business logic cho trading bot
"""

import logging
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime

from src.data.vn_alternative_collector import VNAlternativeCollector
from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.analysis.fundamental_analysis import FundamentalAnalyzer
from src.analysis.sentiment_analysis import SentimentAnalyzer
from src.analysis.advanced_technical import AdvancedTechnicalAnalyzer
from src.analysis.options_analysis import OptionsAnalyzer
from src.analysis.backtesting import Backtester
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager
from src.ai.investment_advisor import AIInvestmentAdvisor
from src.ai.gpt_assistant import GPTAssistant
from src.ai.claude_assistant import ClaudeAssistant
from .config import ConfigManager

class TradingService:
    """Core trading service - centralized business logic"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize configuration
        self.config = ConfigManager()
        
        # Initialize all components
        self._init_components()
        
    def _init_components(self):
        """Initialize all trading components"""
        # Data collectors
        self.vn_collector = VNAlternativeCollector()
        self.us_collector = DataCollector()
        
        # Analysis components
        self.analyzer = TechnicalAnalyzer()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.advanced_analyzer = AdvancedTechnicalAnalyzer()
        self.options_analyzer = OptionsAnalyzer()
        
        # ML & AI components
        self.predictor = PredictionModels()
        self.ai_advisor = AIInvestmentAdvisor()
        
        # Get AI config
        ai_config = self.config.get_ai_config()
        self.gpt_assistant = GPTAssistant(model_name=ai_config.get('gpt_model', 'gpt_assistant:latest'))
        
        # Risk & Strategy components
        self.risk_manager = RiskManager()
        self.backtester = Backtester()
        
        # Initialize Claude Assistant
        try:
            self.claude_assistant = ClaudeAssistant()
            self.logger.info("Claude Assistant initialized successfully")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Claude Assistant: {e}")
            self.claude_assistant = None
    
    def get_stock_data(self, symbol: str, market: str = None, period: str = None) -> pd.DataFrame:
        """Get stock data with market detection"""
        try:
            # Use config defaults if not provided
            if market is None:
                market = self.config.get('trading.default_market', 'US')
            if period is None:
                period = self.config.get('trading.default_period', '6mo')
            
            if market == "VN" or symbol.endswith('.VN') or len(symbol) <= 3:
                return self.vn_collector.get_vn_stock_data_yahoo(symbol, period=period)
            else:
                return self.us_collector.get_stock_data(symbol, period=period)
        except Exception as e:
            self.logger.error(f"Error getting data for {symbol}: {e}")
            return pd.DataFrame()
    
    def quick_analysis(self, symbol: str, market: str = "US") -> Dict:
        """Quick analysis for busy traders"""
        try:
            data = self.get_stock_data(symbol, market)
            if data.empty:
                return {"error": f"Không thể lấy dữ liệu cho {symbol}"}
            
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
            
            return {
                "symbol": symbol,
                "market": market,
                "current_price": data['Close'].iloc[-1],
                "change": data['Returns'].iloc[-1] * 100 if 'Returns' in data.columns else 0,
                "signals": signals,
                "valuation": valuation_ratios,
                "risk": risk_report
            }
        except Exception as e:
            self.logger.error(f"Error in quick analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def comprehensive_analysis(self, symbol: str, market: str = "US") -> Dict:
        """Comprehensive AI analysis"""
        try:
            data = self.get_stock_data(symbol, market)
            if data.empty:
                return {"error": f"Không thể lấy dữ liệu cho {symbol}"}
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            
            # AI recommendation
            recommendation = self.ai_advisor.generate_recommendation(
                symbol, data, signals, risk_report, market
            )
            
            return {
                "symbol": symbol,
                "market": market,
                "current_price": data['Close'].iloc[-1],
                "change": data['Returns'].iloc[-1] * 100 if 'Returns' in data.columns else 0,
                "signals": signals,
                "risk": risk_report,
                "recommendation": recommendation
            }
        except Exception as e:
            self.logger.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def fundamental_analysis(self, symbol: str, market: str = "US") -> Dict:
        """Fundamental analysis"""
        try:
            return self.fundamental_analyzer.generate_fundamental_report(symbol, market)
        except Exception as e:
            self.logger.error(f"Error in fundamental analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def sentiment_analysis(self, symbol: str, market: str = "US") -> Dict:
        """Sentiment analysis"""
        try:
            return self.sentiment_analyzer.generate_market_sentiment_report(symbol, market)
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def risk_analysis(self, symbol: str, market: str = "US") -> Dict:
        """Risk analysis"""
        try:
            data = self.get_stock_data(symbol, market)
            if data.empty:
                return {"error": f"Không thể lấy dữ liệu cho {symbol}"}
            
            return self.risk_manager.generate_risk_report(data, symbol)
        except Exception as e:
            self.logger.error(f"Error in risk analysis for {symbol}: {e}")
            return {"error": str(e)}
    
    def portfolio_optimization(self, symbols: List[str], market: str = "US") -> Dict:
        """Portfolio optimization"""
        try:
            # Get data for all symbols
            portfolio_data = {}
            for symbol in symbols:
                data = self.get_stock_data(symbol, market)
                if not data.empty:
                    portfolio_data[symbol] = data
            
            if len(portfolio_data) < 2:
                return {"error": "Cần ít nhất 2 cổ phiếu để tối ưu portfolio"}
            
            return self.risk_manager.optimize_portfolio(portfolio_data)
        except Exception as e:
            self.logger.error(f"Error in portfolio optimization: {e}")
            return {"error": str(e)}
    
    def predict_price(self, symbol: str, model: str = "lstm", market: str = "US") -> Dict:
        """Price prediction"""
        try:
            data = self.get_stock_data(symbol, market)
            if data.empty:
                return {"error": f"Không thể lấy dữ liệu cho {symbol}"}
            
            return self.predictor.predict(data, symbol, model)
        except Exception as e:
            self.logger.error(f"Error in price prediction for {symbol}: {e}")
            return {"error": str(e)}
    
    def backtest_strategy(self, symbol: str, strategy: str, capital: float = 10000, market: str = "US") -> Dict:
        """Strategy backtesting"""
        try:
            data = self.get_stock_data(symbol, market)
            if data.empty:
                return {"error": f"Không thể lấy dữ liệu cho {symbol}"}
            
            return self.backtester.backtest_strategy(data, strategy, capital)
        except Exception as e:
            self.logger.error(f"Error in backtesting for {symbol}: {e}")
            return {"error": str(e)}
    
    def ask_ai(self, question: str, ai_type: str = "gpt") -> str:
        """Ask AI assistant"""
        try:
            if ai_type == "claude" and self.claude_assistant:
                return self.claude_assistant.ask(question)
            else:
                return self.gpt_assistant.ask(question)
        except Exception as e:
            self.logger.error(f"Error asking AI: {e}")
            return f"❌ Lỗi khi hỏi AI: {str(e)}"

class MarketService:
    """Market data and context service"""
    
    def __init__(self, trading_service: TradingService):
        self.trading_service = trading_service
        self.logger = logging.getLogger(__name__)
    
    def get_market_overview(self, market: str = "US") -> Dict:
        """Get market overview"""
        try:
            return self.trading_service.sentiment_analyzer.generate_market_sentiment_report(market=market)
        except Exception as e:
            self.logger.error(f"Error getting market overview: {e}")
            return {"error": str(e)}
    
    def get_sector_rotation(self, market: str = "US") -> Dict:
        """Get sector rotation analysis"""
        try:
            return self.trading_service.sentiment_analyzer.get_sector_rotation(market)
        except Exception as e:
            self.logger.error(f"Error getting sector rotation: {e}")
            return {"error": str(e)}

class ConfigurationService:
    """Configuration management service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        return {
            "default_period": "6mo",
            "default_market": "US",
            "risk_thresholds": {
                "high_volatility": 0.3,
                "max_drawdown": -0.2,
                "min_sharpe": 0.5
            },
            "trading_hours": {
                "vn_open": "09:00",
                "vn_close": "15:00",
                "us_open": "09:30",
                "us_close": "16:00"
            }
        }
    
    def get_config(self, key: str = None) -> Any:
        """Get configuration value"""
        if key:
            return self.config.get(key)
        return self.config
