import json
import requests
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FinGPTResponse:
    """Response structure for FinGPT model"""
    answer: str
    confidence: float
    source: str
    model_version: str

class FinGPTModel:
    """Custom FinGPT model for Vietnamese financial analysis"""
    
    def __init__(self, model_name: str = "fingpt:latest", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.financial_knowledge = self._load_financial_knowledge()
        
    def _load_financial_knowledge(self) -> Dict:
        """Load Vietnamese financial knowledge base"""
        return {
            "technical_indicators": {
                "RSI": {
                    "name": "Relative Strength Index",
                    "description": "Chỉ số sức mạnh tương đối, đo lường tốc độ và mức độ thay đổi giá",
                    "formula": "RSI = 100 - (100 / (1 + RS)), RS = Average Gain / Average Loss",
                    "interpretation": "RSI > 70: Overbought (quá mua), RSI < 30: Oversold (quá bán)",
                    "usage": "Xác định điểm vào lệnh khi oversold (RSI < 30) hoặc thoát lệnh khi overbought (RSI > 70)"
                },
                "MACD": {
                    "name": "Moving Average Convergence Divergence",
                    "description": "Chỉ báo momentum, so sánh hai đường trung bình động",
                    "formula": "MACD = EMA(12) - EMA(26), Signal = EMA(9) của MACD",
                    "interpretation": "MACD > Signal: Bullish, MACD < Signal: Bearish",
                    "usage": "Xác định xu hướng và momentum. Tín hiệu mua khi MACD vượt Signal, bán khi xuống dưới Signal"
                },
                "Bollinger_Bands": {
                    "name": "Bollinger Bands",
                    "description": "Dải băng Bollinger, đo lường biến động giá",
                    "formula": "Upper = SMA(20) + 2*StdDev, Lower = SMA(20) - 2*StdDev",
                    "interpretation": "Giá chạm dải trên: Overbought, Giá chạm dải dưới: Oversold",
                    "usage": "Xác định biến động giá và điểm vào lệnh. Giá chạm dải dưới có thể mua, chạm dải trên có thể bán"
                }
            },
            "vn_market": {
                "popular_stocks": ["VNM", "TCB", "HPG", "VCB", "BID", "FPT", "VIC", "VHM"],
                "sectors": {
                    "banking": ["TCB", "VCB", "BID", "ACB", "MBB"],
                    "consumer": ["VNM", "HPG", "MSN", "SAB"],
                    "tech": ["FPT", "VNG", "MWG"],
                    "real_estate": ["VIC", "VHM", "NVL", "DXG"]
                }
            },
            "risk_metrics": {
                "VaR": "Value at Risk - Mức lỗ tối đa có thể xảy ra",
                "Sharpe_Ratio": "Đo lường lợi nhuận so với rủi ro. > 1: Tốt, > 2: Rất tốt",
                "Max_Drawdown": "Mức sụt giảm tối đa từ đỉnh",
                "Volatility": "Độ biến động giá, đo lường rủi ro"
            }
        }
    
    def ask(self, question: str) -> FinGPTResponse:
        """Ask question to FinGPT model"""
        try:
            # Try Ollama API first
            response = self._call_ollama(question)
            if response:
                return response
            
            # Fallback to knowledge base
            return self._fallback_response(question)
            
        except Exception as e:
            logging.error(f"Error in FinGPT ask: {e}")
            return self._fallback_response(question)
    
    def _call_ollama(self, question: str) -> Optional[FinGPTResponse]:
        """Call Ollama API"""
        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model_name,
                "prompt": self._create_prompt(question),
                "stream": False
            }
            
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return FinGPTResponse(
                    answer=result.get("response", ""),
                    confidence=0.9,
                    source="ollama",
                    model_version=self.model_name
                )
        except Exception as e:
            logging.warning(f"Ollama API failed: {e}")
        return None
    
    def _create_prompt(self, question: str) -> str:
        """Create optimized prompt for financial analysis"""
        return f"""Bạn là FinGPT - AI chuyên gia tài chính Việt Nam. 
Hãy trả lời câu hỏi sau bằng tiếng Việt, tập trung vào thị trường Việt Nam:

Câu hỏi: {question}

Hãy trả lời chi tiết, chính xác và hữu ích cho nhà đầu tư Việt Nam."""
    
    def _fallback_response(self, question: str) -> FinGPTResponse:
        """Fallback response using knowledge base"""
        question_lower = question.lower()
        
        # Check for technical indicators
        for indicator, info in self.financial_knowledge["technical_indicators"].items():
            if indicator.lower() in question_lower:
                answer = f"{info['name']}: {info['description']}. {info['interpretation']}. {info['usage']}"
                return FinGPTResponse(
                    answer=answer,
                    confidence=0.8,
                    source="knowledge_base",
                    model_version="fingpt_fallback"
                )
        
        # Check for risk metrics
        for metric, description in self.financial_knowledge["risk_metrics"].items():
            if metric.lower() in question_lower:
                return FinGPTResponse(
                    answer=f"{metric}: {description}",
                    confidence=0.8,
                    source="knowledge_base", 
                    model_version="fingpt_fallback"
                )
        
        # Default response
        return FinGPTResponse(
            answer="Tôi là FinGPT - AI chuyên gia tài chính. Hiện tại tôi đang được phát triển để hỗ trợ tốt hơn cho thị trường Việt Nam.",
            confidence=0.5,
            source="fallback",
            model_version="fingpt_fallback"
        )
    
    def explain_indicator(self, indicator: str) -> FinGPTResponse:
        """Explain technical indicator"""
        indicator_lower = indicator.lower()
        
        for key, info in self.financial_knowledge["technical_indicators"].items():
            if key.lower() in indicator_lower or indicator_lower in key.lower():
                answer = f"""📊 **{info['name']}**
                
**Mô tả:** {info['description']}
**Cách hiểu:** {info['interpretation']}
**Công thức:** {info['formula']}
**Cách sử dụng:** {info['usage']}"""
                
                return FinGPTResponse(
                    answer=answer,
                    confidence=0.9,
                    source="knowledge_base",
                    model_version="fingpt"
                )
        
        return FinGPTResponse(
            answer=f"❌ Chưa có thông tin về chỉ báo {indicator}. Các chỉ báo có sẵn: RSI, MACD, Bollinger Bands.",
            confidence=0.3,
            source="fallback",
            model_version="fingpt_fallback"
        )
    
    def get_investment_tips(self, topic: str = "general") -> FinGPTResponse:
        """Get investment tips"""
        tips = {
            "general": [
                "Luôn đa dạng hóa portfolio để giảm rủi ro",
                "Không đầu tư quá 5-10% vào một cổ phiếu",
                "Sử dụng stop loss để bảo vệ vốn",
                "Đầu tư dài hạn thay vì timing thị trường",
                "Theo dõi các chỉ số cơ bản của công ty"
            ],
            "technical": [
                "Kết hợp nhiều chỉ báo kỹ thuật để xác nhận tín hiệu",
                "Không chỉ dựa vào một chỉ báo duy nhất",
                "Chú ý đến khối lượng giao dịch",
                "Xem xét xu hướng dài hạn trước khi vào lệnh",
                "Sử dụng support và resistance levels"
            ],
            "risk": [
                "Luôn tính toán risk/reward ratio trước khi vào lệnh",
                "Không sử dụng đòn bẩy quá cao",
                "Theo dõi các chỉ số rủi ro như VaR, Max Drawdown",
                "Có kế hoạch thoát lệnh rõ ràng",
                "Không để cảm xúc chi phối quyết định"
            ]
        }
        
        topic_tips = tips.get(topic, tips["general"])
        answer = f"💡 **Lời khuyên đầu tư về {topic}:**\n\n" + "\n".join([f"{i+1}. {tip}" for i, tip in enumerate(topic_tips)])
        
        return FinGPTResponse(
            answer=answer,
            confidence=0.9,
            source="knowledge_base",
            model_version="fingpt"
        ) 