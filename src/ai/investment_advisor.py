"""
AI Investment Advisor
AI chuyên gia tư vấn đầu tư dựa trên phân tích kỹ thuật và cơ bản
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json

@dataclass
class InvestmentRecommendation:
    """Class chứa khuyến nghị đầu tư"""
    symbol: str
    recommendation: str  # BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL
    confidence: float  # 0-1
    reasoning: List[str]
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    time_horizon: str = "3-6 months"
    risk_level: str = "MEDIUM"
    market_sentiment: str = "NEUTRAL"

class AIInvestmentAdvisor:
    """AI chuyên gia tư vấn đầu tư"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Định nghĩa các ngưỡng
        self.thresholds = {
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            'macd_bullish': 0.5,
            'macd_bearish': -0.5,
            'volatility_high': 0.4,
            'volatility_low': 0.15,
            'sharpe_good': 1.0,
            'sharpe_poor': 0.0,
            'drawdown_critical': -0.25,
            'drawdown_warning': -0.15,
            'var_critical': -0.03,
            'var_warning': -0.02
        }
        
        # Trọng số cho các yếu tố
        self.weights = {
            'technical_analysis': 0.35,
            'risk_metrics': 0.25,
            'price_action': 0.20,
            'market_sentiment': 0.15,
            'volume_analysis': 0.05
        }
    
    def analyze_technical_signals(self, signals: Dict) -> Tuple[float, List[str]]:
        """Phân tích tín hiệu kỹ thuật"""
        score = 0.0
        reasons = []
        
        if 'error' in signals:
            return 0.0, ["Không thể phân tích tín hiệu kỹ thuật"]
        
        # RSI Analysis
        rsi_signal = signals.get('RSI', 'NEUTRAL')
        if 'BUY' in rsi_signal:
            score += 0.3
            reasons.append("RSI cho thấy tín hiệu mua (oversold)")
        elif 'SELL' in rsi_signal:
            score -= 0.3
            reasons.append("RSI cho thấy tín hiệu bán (overbought)")
        
        # MACD Analysis
        macd_signal = signals.get('MACD', 'NEUTRAL')
        if 'BUY' in macd_signal:
            score += 0.25
            reasons.append("MACD cho thấy momentum tăng")
        elif 'SELL' in macd_signal:
            score -= 0.25
            reasons.append("MACD cho thấy momentum giảm")
        
        # Bollinger Bands
        bb_signal = signals.get('BB', 'NEUTRAL')
        if 'BUY' in bb_signal:
            score += 0.2
            reasons.append("Giá gần dải Bollinger dưới (cơ hội mua)")
        elif 'SELL' in bb_signal:
            score -= 0.2
            reasons.append("Giá gần dải Bollinger trên (cơ hội bán)")
        
        # Moving Averages
        ma_signal = signals.get('MA', 'NEUTRAL')
        if 'BUY' in ma_signal:
            score += 0.25
            reasons.append("Đường trung bình động hỗ trợ xu hướng tăng")
        elif 'SELL' in ma_signal:
            score -= 0.25
            reasons.append("Đường trung bình động cho thấy xu hướng giảm")
        
        return score, reasons
    
    def analyze_risk_metrics(self, risk_report: Dict) -> Tuple[float, List[str]]:
        """Phân tích chỉ số rủi ro"""
        score = 0.0
        reasons = []
        
        if 'error' in risk_report:
            return 0.0, ["Không thể phân tích rủi ro"]
        
        # Sharpe Ratio
        sharpe = risk_report.get('sharpe_ratio', 0)
        if sharpe > self.thresholds['sharpe_good']:
            score += 0.3
            reasons.append(f"Sharpe Ratio tốt ({sharpe:.2f}) - Lợi nhuận cao so với rủi ro")
        elif sharpe < self.thresholds['sharpe_poor']:
            score -= 0.3
            reasons.append(f"Sharpe Ratio thấp ({sharpe:.2f}) - Rủi ro cao so với lợi nhuận")
        
        # Max Drawdown
        max_dd = risk_report.get('max_drawdown', 0)
        if max_dd > self.thresholds['drawdown_critical']:
            score -= 0.4
            reasons.append(f"Drawdown quá cao ({max_dd:.1%}) - Rủi ro lớn")
        elif max_dd > self.thresholds['drawdown_warning']:
            score -= 0.2
            reasons.append(f"Drawdown cao ({max_dd:.1%}) - Cần thận trọng")
        
        # VaR
        var_95 = risk_report.get('var_95', 0)
        if var_95 < self.thresholds['var_critical']:
            score -= 0.3
            reasons.append(f"VaR cao ({var_95:.1%}) - Rủi ro thua lỗ lớn")
        
        # Total Return
        total_return = risk_report.get('total_return', 0)
        if total_return > 10:
            score += 0.2
            reasons.append(f"Lợi nhuận tốt ({total_return:.1f}%)")
        elif total_return < -10:
            score -= 0.2
            reasons.append(f"Thua lỗ lớn ({total_return:.1f}%)")
        
        return score, reasons
    
    def analyze_price_action(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """Phân tích hành động giá"""
        score = 0.0
        reasons = []
        
        if len(data) < 20:
            return 0.0, ["Không đủ dữ liệu để phân tích hành động giá"]
        
        # Recent price trend
        recent_prices = data['Close'].tail(20)
        price_trend = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]
        
        if price_trend > 0.05:  # Tăng >5%
            score += 0.3
            reasons.append("Xu hướng giá tăng mạnh trong 20 ngày gần nhất")
        elif price_trend < -0.05:  # Giảm >5%
            score -= 0.3
            reasons.append("Xu hướng giá giảm mạnh trong 20 ngày gần nhất")
        
        # Support/Resistance levels
        current_price = data['Close'].iloc[-1]
        high_20d = data['High'].tail(20).max()
        low_20d = data['Low'].tail(20).min()
        
        if current_price > high_20d * 0.95:
            score += 0.2
            reasons.append("Giá đang test mức kháng cự cao")
        elif current_price < low_20d * 1.05:
            score -= 0.2
            reasons.append("Giá đang test mức hỗ trợ thấp")
        
        # Volume analysis
        recent_volume = data['Volume'].tail(10).mean()
        avg_volume = data['Volume'].tail(50).mean()
        
        if recent_volume > avg_volume * 1.5:
            score += 0.1
            reasons.append("Khối lượng giao dịch tăng cao - Tín hiệu tích cực")
        elif recent_volume < avg_volume * 0.5:
            score -= 0.1
            reasons.append("Khối lượng giao dịch thấp - Thiếu sức mua")
        
        return score, reasons
    
    def analyze_market_sentiment(self, symbol: str, market_type: str = "VN") -> Tuple[float, List[str]]:
        """Phân tích tâm lý thị trường"""
        score = 0.0
        reasons = []
        
        # Market sentiment based on symbol type
        if market_type == "VN":
            # VN market sentiment
            blue_chips = ['VNM', 'TCB', 'HPG', 'FPT', 'VIC', 'VHM']
            if symbol in blue_chips:
                score += 0.2
                reasons.append("Cổ phiếu blue-chip - Ít rủi ro hơn")
            
            # Sector analysis
            if symbol in ['VNM', 'VIC', 'VHM']:
                score += 0.1
                reasons.append("Thuộc nhóm tiêu dùng - Ổn định")
            elif symbol in ['TCB', 'VCB', 'BID']:
                score += 0.1
                reasons.append("Thuộc nhóm ngân hàng - Tăng trưởng tốt")
        else:
            # US market sentiment
            tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            if symbol in tech_stocks:
                score += 0.2
                reasons.append("Cổ phiếu công nghệ - Tiềm năng tăng trưởng cao")
        
        return score, reasons
    
    def calculate_target_price(self, data: pd.DataFrame, recommendation: str) -> Tuple[float, float]:
        """Tính toán giá mục tiêu và stop loss"""
        current_price = data['Close'].iloc[-1]
        
        if recommendation in ['STRONG_BUY', 'BUY']:
            # Target: 15-20% above current price
            target_price = current_price * 1.15
            stop_loss = current_price * 0.92  # 8% below current
        elif recommendation in ['STRONG_SELL', 'SELL']:
            # Target: 15-20% below current price
            target_price = current_price * 0.85
            stop_loss = current_price * 1.08  # 8% above current
        else:  # HOLD
            target_price = current_price * 1.05
            stop_loss = current_price * 0.95
        
        return target_price, stop_loss
    
    def determine_time_horizon(self, signals: Dict, risk_report: Dict) -> str:
        """Xác định khung thời gian đầu tư"""
        # Analyze volatility and trend strength
        volatility = risk_report.get('volatility_annual', 0)
        
        if volatility > 0.4:
            return "1-3 months"  # High volatility - short term
        elif volatility > 0.25:
            return "3-6 months"  # Medium volatility - medium term
        else:
            return "6-12 months"  # Low volatility - long term
    
    def determine_risk_level(self, risk_report: Dict) -> str:
        """Xác định mức độ rủi ro"""
        sharpe = risk_report.get('sharpe_ratio', 0)
        max_dd = risk_report.get('max_drawdown', 0)
        var_95 = risk_report.get('var_95', 0)
        
        risk_score = 0
        
        if sharpe < 0:
            risk_score += 2
        elif sharpe < 0.5:
            risk_score += 1
        
        if max_dd < -0.25:
            risk_score += 2
        elif max_dd < -0.15:
            risk_score += 1
        
        if var_95 < -0.03:
            risk_score += 1
        
        if risk_score >= 4:
            return "HIGH"
        elif risk_score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_recommendation(self, symbol: str, data: pd.DataFrame, 
                              signals: Dict, risk_report: Dict, 
                              market_type: str = "VN") -> InvestmentRecommendation:
        """Tạo khuyến nghị đầu tư tổng hợp"""
        
        # Analyze different factors
        tech_score, tech_reasons = self.analyze_technical_signals(signals)
        risk_score, risk_reasons = self.analyze_risk_metrics(risk_report)
        price_score, price_reasons = self.analyze_price_action(data)
        sentiment_score, sentiment_reasons = self.analyze_market_sentiment(symbol, market_type)
        
        # Calculate weighted score
        total_score = (
            tech_score * self.weights['technical_analysis'] +
            risk_score * self.weights['risk_metrics'] +
            price_score * self.weights['price_action'] +
            sentiment_score * self.weights['market_sentiment']
        )
        
        # Determine recommendation
        if total_score >= 0.6:
            recommendation = "STRONG_BUY"
        elif total_score >= 0.2:
            recommendation = "BUY"
        elif total_score >= -0.2:
            recommendation = "HOLD"
        elif total_score >= -0.6:
            recommendation = "SELL"
        else:
            recommendation = "STRONG_SELL"
        
        # Calculate confidence
        confidence = min(abs(total_score) + 0.3, 0.95)
        
        # Combine all reasons
        all_reasons = tech_reasons + risk_reasons + price_reasons + sentiment_reasons
        
        # Calculate target price and stop loss
        target_price, stop_loss = self.calculate_target_price(data, recommendation)
        
        # Determine time horizon and risk level
        time_horizon = self.determine_time_horizon(signals, risk_report)
        risk_level = self.determine_risk_level(risk_report)
        
        # Determine market sentiment
        if total_score > 0.3:
            market_sentiment = "BULLISH"
        elif total_score < -0.3:
            market_sentiment = "BEARISH"
        else:
            market_sentiment = "NEUTRAL"
        
        return InvestmentRecommendation(
            symbol=symbol,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=all_reasons,
            target_price=target_price,
            stop_loss=stop_loss,
            time_horizon=time_horizon,
            risk_level=risk_level,
            market_sentiment=market_sentiment
        )
    
    def get_investment_strategy(self, recommendation: InvestmentRecommendation) -> Dict:
        """Đưa ra chiến lược đầu tư chi tiết"""
        
        strategy = {
            'action': recommendation.recommendation,
            'position_size': self._calculate_position_size(recommendation),
            'entry_strategy': self._get_entry_strategy(recommendation),
            'exit_strategy': self._get_exit_strategy(recommendation),
            'risk_management': self._get_risk_management(recommendation)
        }
        
        return strategy
    
    def _calculate_position_size(self, recommendation: InvestmentRecommendation) -> str:
        """Tính toán kích thước vị thế"""
        if recommendation.recommendation == "STRONG_BUY":
            return "10-15% portfolio"
        elif recommendation.recommendation == "BUY":
            return "5-10% portfolio"
        elif recommendation.recommendation == "HOLD":
            return "Giữ nguyên vị thế"
        elif recommendation.recommendation == "SELL":
            return "Giảm 50% vị thế"
        else:  # STRONG_SELL
            return "Đóng toàn bộ vị thế"
    
    def _get_entry_strategy(self, recommendation: InvestmentRecommendation) -> str:
        """Chiến lược vào lệnh"""
        if recommendation.recommendation in ['STRONG_BUY', 'BUY']:
            return f"Vào lệnh từng phần: 50% ngay, 50% khi giá về {recommendation.stop_loss:.0f}"
        else:
            return "Không vào lệnh mới"
    
    def _get_exit_strategy(self, recommendation: InvestmentRecommendation) -> str:
        """Chiến lược thoát lệnh"""
        if recommendation.recommendation in ['STRONG_BUY', 'BUY']:
            return f"Chốt lời tại {recommendation.target_price:.0f}, cắt lỗ tại {recommendation.stop_loss:.0f}"
        elif recommendation.recommendation in ['STRONG_SELL', 'SELL']:
            return f"Thoát lệnh khi giá về {recommendation.target_price:.0f}"
        else:
            return "Giữ nguyên, theo dõi tín hiệu"
    
    def _get_risk_management(self, recommendation: InvestmentRecommendation) -> str:
        """Quản lý rủi ro"""
        if recommendation.risk_level == "HIGH":
            return "Sử dụng stop loss chặt chẽ, không đòn bẩy"
        elif recommendation.risk_level == "MEDIUM":
            return "Stop loss vừa phải, đa dạng hóa"
        else:
            return "Có thể tăng vị thế, ít rủi ro"

# Example usage
if __name__ == "__main__":
    # Test AI advisor
    advisor = AIInvestmentAdvisor()
    print("🤖 AI Investment Advisor đã sẵn sàng!") 