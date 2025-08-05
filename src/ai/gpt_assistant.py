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
    
    def __init__(self, model_name: str = "gpt_assistant_v3:latest"):
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        # Enhanced knowledge base for fallback
        self.financial_knowledge = {
            "technical_indicators": {
                "RSI": "Chỉ số sức mạnh tương đối (Relative Strength Index). RSI > 70: Overbought (quá mua), RSI < 30: Oversold (quá bán). RSI = 50: Trung tính. Sử dụng để xác định điểm vào lệnh và thoát lệnh.",
                "MACD": "Chỉ báo momentum (Moving Average Convergence Divergence). MACD > Signal: Tín hiệu tăng (Bullish), MACD < Signal: Tín hiệu giảm (Bearish). Histogram > 0: Momentum tăng, Histogram < 0: Momentum giảm.",
                "Bollinger_Bands": "Đo lường biến động giá. Giá chạm dải trên: Overbought, giá chạm dải dưới: Oversold. Dải băng thu hẹp: Biến động thấp, dải băng mở rộng: Biến động cao.",
                "Moving_Averages": "Xác định xu hướng. Giá > MA: Uptrend (xu hướng tăng), giá < MA: Downtrend (xu hướng giảm). MA ngắn hạn > MA dài hạn: Tín hiệu tăng.",
                "Stochastic": "Chỉ báo momentum. %K > 80: Overbought, %K < 20: Oversold. %K > %D: Tín hiệu tăng, %K < %D: Tín hiệu giảm.",
                "ATR": "Average True Range - đo lường biến động. ATR cao: Biến động lớn, ATR thấp: Biến động nhỏ. Dùng để đặt stop loss.",
                "Volume": "Khối lượng giao dịch. Volume cao + giá tăng: Xác nhận xu hướng tăng. Volume cao + giá giảm: Xác nhận xu hướng giảm."
            },
            "risk_metrics": {
                "Sharpe_Ratio": "Đo lường lợi nhuận so với rủi ro. > 1: Tốt, > 2: Rất tốt, < 0: Kém. Càng cao càng tốt.",
                "Sortino_Ratio": "Tương tự Sharpe nhưng chỉ xem xét downside risk. > 1: Tốt, càng cao càng tốt.",
                "Max_Drawdown": "Mức giảm tối đa từ đỉnh đến đáy. Càng thấp càng tốt. < -20%: Rủi ro cao.",
                "VaR": "Value at Risk - Giá trị rủi ro, mức thua lỗ tối đa có thể trong 95% trường hợp. Càng thấp càng tốt.",
                "CVaR": "Conditional VaR - Mức thua lỗ trung bình khi vượt quá VaR. Càng thấp càng tốt.",
                "Beta": "Đo lường biến động so với thị trường. Beta > 1: Biến động cao hơn thị trường, Beta < 1: Biến động thấp hơn thị trường."
            },
            "vietnam_market": {
                "VN_Index": "Chỉ số chính của thị trường Việt Nam. Tăng: Thị trường tốt, Giảm: Thị trường xấu.",
                "Blue_chip": "Cổ phiếu lớn, ổn định như VNM, TCB, HPG, FPT, VIC, VHM.",
                "Mid_cap": "Cổ phiếu vừa như VRE, MWG, VPB, ACB, BID.",
                "Small_cap": "Cổ phiếu nhỏ, rủi ro cao nhưng tiềm năng tăng trưởng lớn.",
                "Banking": "Ngành ngân hàng: TCB, VPB, ACB, BID, VCB, TPB.",
                "Consumer": "Ngành tiêu dùng: VNM, MWG, VRE, MSN, KDC.",
                "Technology": "Ngành công nghệ: FPT, VNG, TMA, GDT.",
                "Real_Estate": "Ngành bất động sản: VIC, VHM, NVL, KDH, DIG."
            }
        }
    
    def _call_ollama(self, question: str) -> Optional[GPTResponse]:
        """Call Ollama using subprocess"""
        try:
            cmd = ["ollama", "run", self.model_name, self._create_prompt(question)]
            self.logger.info(f"Calling Ollama with command: {' '.join(cmd[:3])}...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            self.logger.info(f"Ollama return code: {result.returncode}")
            if result.stderr:
                self.logger.warning(f"Ollama stderr: {result.stderr}")
            
            if result.returncode == 0:
                answer = result.stdout.strip()
                if answer:
                    self.logger.info(f"Ollama response length: {len(answer)} characters")
                    return GPTResponse(
                        answer=answer,
                        confidence=0.9,
                        source="ollama",
                        model_version=self.model_name
                    )
                else:
                    self.logger.warning("Ollama returned empty response")
            else:
                self.logger.warning(f"Ollama subprocess failed with return code {result.returncode}: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Ollama subprocess timeout for question: {question[:50]}...")
        except FileNotFoundError:
            self.logger.warning("Ollama not found in PATH")
        except Exception as e:
            self.logger.warning(f"Ollama subprocess failed: {e}")
            import traceback
            self.logger.warning(f"Traceback: {traceback.format_exc()}")
        return None
    
    def _create_prompt(self, question: str) -> str:
        """Create optimized prompt for financial analysis with Llama2"""
        return f"""<s>[INST] Bạn là AI chuyên gia tài chính Việt Nam. Bạn PHẢI trả lời bằng TIẾNG VIỆT.

Nhiệm vụ: Trả lời câu hỏi về tài chính, đầu tư, phân tích kỹ thuật bằng TIẾNG VIỆT.

Yêu cầu QUAN TRỌNG:
- BẮT BUỘC trả lời bằng TIẾNG VIỆT
- Trả lời chi tiết, chính xác và dễ hiểu
- Tập trung vào thị trường Việt Nam
- Đưa ra lời khuyên thực tế và hữu ích
- Sử dụng emoji để dễ đọc
- Giữ câu trả lời trong khoảng 200-400 từ
- KHÔNG được trả lời bằng tiếng Anh

Câu hỏi: {question}

Hãy trả lời bằng TIẾNG VIỆT: [/INST]"""
    
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
        return {
            "type": "fallback",
            "answer": """🤖 **Ollama không khả dụng**

Hiện tại Ollama đang gặp sự cố và không thể trả lời câu hỏi của bạn.

**Có thể do:**
- Ollama service chưa được khởi động
- Model không tồn tại hoặc bị lỗi
- Thiếu quyền truy cập

**Cách khắc phục:**
1. Kiểm tra Ollama: `ollama list`
2. Khởi động Ollama service
3. Thử lại sau vài phút

💡 **Lưu ý:** Hãy thử lại sau khi Ollama hoạt động bình thường.""",
            "confidence": 0.0
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
            source_info = f"🤖 AI Model: {analysis.get('model_version', 'Unknown')}"
            confidence = analysis.get('confidence', 0)
            confidence_emoji = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.6 else "🔴"
            return f"{source_info} {confidence_emoji} Độ tin cậy: {confidence:.0%}\n\n{analysis['answer']}"
        
        elif analysis["type"] == "fallback":
            return f"📚 Fallback Response (Ollama không khả dụng)\n\n{analysis['answer']}"
        
        else:
            return f"💡 Response:\n\n{analysis['answer']}"

# Example usage
if __name__ == "__main__":
    assistant = GPTAssistant()
    print("🤖 GPT Assistant đã sẵn sàng!")
    
    # Test
    question = "RSI là gì và cách sử dụng?"
    result = assistant.analyze_question(question)
    print(assistant.format_response(result)) 