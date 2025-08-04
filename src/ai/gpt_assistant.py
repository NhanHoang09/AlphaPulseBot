"""
AI GPT Assistant với Ollama
AI trợ lý thông minh sử dụng Ollama để hỏi đáp và giải thích kỹ thuật đầu tư
"""

import logging
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class GPTResponse:
    """Response structure for GPT Assistant"""
    answer: str
    confidence: float
    source: str
    model_version: str

class GPTAssistant:
    """AI GPT Assistant cho tài chính sử dụng Ollama"""
    
    def __init__(self, model_name: str = "llama2:7b"):
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        # Minimal knowledge base for fallback
        self.financial_knowledge = {
            "technical_indicators": {
                "RSI": "Chỉ số sức mạnh tương đối, RSI > 70: Overbought, RSI < 30: Oversold",
                "MACD": "Chỉ báo momentum, MACD > Signal: Bullish, MACD < Signal: Bearish",
                "Bollinger_Bands": "Đo lường biến động giá, giá chạm dải trên/dưới: Overbought/Oversold",
                "Moving_Averages": "Xác định xu hướng, giá > MA: Uptrend, giá < MA: Downtrend"
            },
            "risk_metrics": {
                "Sharpe_Ratio": "Đo lường lợi nhuận so với rủi ro, > 1: Tốt, > 2: Rất tốt",
                "Max_Drawdown": "Mức giảm tối đa từ đỉnh đến đáy, càng thấp càng tốt",
                "VaR": "Giá trị rủi ro, mức thua lỗ tối đa có thể"
            }
        }
    
    def _call_ollama(self, question: str) -> Optional[GPTResponse]:
        """Call Ollama using subprocess"""
        try:
            cmd = ["ollama", "run", self.model_name, self._create_prompt(question)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                answer = result.stdout.strip()
                if answer:
                    return GPTResponse(
                        answer=answer,
                        confidence=0.9,
                        source="ollama",
                        model_version=self.model_name
                    )
            else:
                self.logger.warning(f"Ollama subprocess failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Ollama subprocess timeout for question: {question[:50]}...")
        except FileNotFoundError:
            self.logger.warning("Ollama not found in PATH")
        except Exception as e:
            self.logger.warning(f"Ollama subprocess failed: {e}")
        return None
    
    def _create_prompt(self, question: str) -> str:
        """Create optimized prompt for financial analysis"""
        return f"""Bạn là AI chuyên gia tài chính Việt Nam. 
Hãy trả lời câu hỏi sau bằng tiếng Việt, tập trung vào thị trường Việt Nam:

Câu hỏi: {question}

Hãy trả lời chi tiết, chính xác và hữu ích cho nhà đầu tư Việt Nam."""
    
    def analyze_question(self, question: str) -> Dict:
        """Phân tích câu hỏi và đưa ra câu trả lời"""
        # Try Ollama first
        ollama_response = self._call_ollama(question)
        if ollama_response and ollama_response.answer.strip():
            return {
                "type": "ollama",
                "answer": ollama_response.answer,
                "confidence": ollama_response.confidence,
                "source": ollama_response.source,
                "model_version": ollama_response.model_version
            }
        
        # Fallback to knowledge base if Ollama fails
        self.logger.warning("Ollama failed, using fallback knowledge base")
        return self._fallback_response(question)
    
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when Ollama fails"""
        question_lower = question.lower()
        
        # Check technical indicators
        for indicator, description in self.financial_knowledge["technical_indicators"].items():
            if indicator.lower() in question_lower:
                return {
                    "type": "fallback",
                    "answer": f"**{indicator}:** {description}",
                    "confidence": 0.7
                }
        
        # Check risk metrics
        for metric, description in self.financial_knowledge["risk_metrics"].items():
            if metric.lower().replace("_", " ") in question_lower:
                return {
                    "type": "fallback",
                    "answer": f"**{metric}:** {description}",
                    "confidence": 0.7
                }
        
        # General response
        return {
            "type": "fallback",
            "answer": "Tôi hiểu câu hỏi của bạn về tài chính. Để có câu trả lời chính xác hơn, bạn có thể hỏi cụ thể về: RSI, MACD, Bollinger Bands, Sharpe Ratio, hoặc các chỉ báo kỹ thuật khác.",
            "confidence": 0.5
        }
    
    def explain_indicator(self, indicator: str) -> Dict:
        """Giải thích chi tiết về một chỉ báo"""
        # Try Ollama first
        question = f"Giải thích chi tiết về chỉ báo {indicator} trong phân tích kỹ thuật"
        ollama_response = self._call_ollama(question)
        if ollama_response and ollama_response.answer.strip():
            return {
                "indicator": indicator,
                "name": f"Giải thích {indicator}",
                "description": ollama_response.answer,
                "source": ollama_response.source,
                "model_version": ollama_response.model_version
            }
        
        # Fallback
        self.logger.warning(f"Ollama failed for indicator {indicator}, using fallback")
        indicator_upper = indicator.upper()
        
        if indicator_upper in self.financial_knowledge["technical_indicators"]:
            return {
                "indicator": indicator,
                "name": f"Giải thích {indicator}",
                "description": self.financial_knowledge["technical_indicators"][indicator_upper],
                "source": "fallback",
                "model_version": "knowledge_base"
            }
        
        return {
            "indicator": indicator,
            "error": f"Chưa có thông tin về chỉ báo {indicator}. Các chỉ báo có sẵn: RSI, MACD, Bollinger Bands, Moving Averages."
        }
    
    def get_investment_tips(self, topic: str = "general") -> List[str]:
        """Đưa ra lời khuyên đầu tư"""
        # Try Ollama first
        question = f"Đưa ra 5 lời khuyên đầu tư về {topic} cho nhà đầu tư Việt Nam"
        ollama_response = self._call_ollama(question)
        if ollama_response and ollama_response.answer.strip():
            # Parse response into tips
            tips_text = ollama_response.answer
            tips_list = []
            lines = tips_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('•') or line.startswith('-') or 
                           any(line.startswith(f"{i}.") for i in range(1, 6))):
                    tip = line.lstrip('•-123456789. ')
                    if tip:
                        tips_list.append(tip)
            
            if tips_list:
                return tips_list[:5]
        
        # Fallback tips
        self.logger.warning(f"Ollama failed for tips {topic}, using fallback")
        return [
            "Luôn đa dạng hóa portfolio để giảm rủi ro",
            "Không đầu tư quá 5-10% vào một cổ phiếu",
            "Sử dụng stop loss để bảo vệ vốn",
            "Đầu tư dài hạn thay vì timing thị trường",
            "Theo dõi các chỉ số cơ bản của công ty"
        ]
    
    def format_response(self, analysis: Dict) -> str:
        """Định dạng câu trả lời"""
        if analysis["type"] == "ollama":
            source_info = f"🤖 **AI Model:** {analysis.get('model_version', 'Unknown')}"
            return f"{source_info}\n\n{analysis['answer']}"
        
        elif analysis["type"] == "fallback":
            return f"📚 **Fallback Response:**\n\n{analysis['answer']}"
        
        else:
            return f"💡 **Response:**\n\n{analysis['answer']}"

# Example usage
if __name__ == "__main__":
    assistant = GPTAssistant()
    print("🤖 GPT Assistant đã sẵn sàng!")
    
    # Test
    question = "RSI là gì và cách sử dụng?"
    result = assistant.analyze_question(question)
    print(assistant.format_response(result)) 