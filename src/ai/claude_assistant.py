"""
Claude AI Assistant cho Telegram Bot
AI trợ lý thông minh sử dụng Claude API để hỏi đáp và phân tích tài chính
"""

import logging
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import anthropic
from anthropic import Anthropic

@dataclass
class ClaudeResponse:
    """Response structure for Claude Assistant"""
    answer: str
    confidence: float
    source: str
    model_version: str
    tokens_used: int

class ClaudeAssistant:
    """AI Claude Assistant cho tài chính sử dụng Claude API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.model = model
        self.logger = logging.getLogger(__name__)
        
        # Initialize Claude client
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required. Set it in environment variables or pass to constructor.")
        
        self.client = Anthropic(api_key=self.api_key)
        
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
    
    def _call_claude_api(self, question: str) -> Optional[ClaudeResponse]:
        """Call Claude API"""
        try:
            prompt = self._create_prompt(question)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            if response.content and len(response.content) > 0:
                answer = response.content[0].text
                return ClaudeResponse(
                    answer=answer,
                    confidence=0.95,
                    source="claude_api",
                    model_version=self.model,
                    tokens_used=response.usage.input_tokens + response.usage.output_tokens
                )
                
        except Exception as e:
            self.logger.error(f"Claude API call failed: {e}")
        return None
    
    def _create_prompt(self, question: str) -> str:
        """Create optimized prompt for financial analysis with Claude"""
        return f"""Bạn là AI chuyên gia tài chính Việt Nam với kiến thức sâu rộng về thị trường chứng khoán Việt Nam.

Nhiệm vụ: Trả lời câu hỏi về tài chính, đầu tư, phân tích kỹ thuật bằng tiếng Việt.

Yêu cầu:
- Trả lời chi tiết, chính xác và dễ hiểu
- Tập trung vào thị trường Việt Nam
- Đưa ra lời khuyên thực tế và hữu ích
- Sử dụng emoji để dễ đọc
- Giữ câu trả lời trong khoảng 200-400 từ
- Định dạng markdown cho dễ đọc

Câu hỏi: {question}

Hãy trả lời:"""
    
    def analyze_question(self, question: str) -> Dict:
        """Analyze financial question using Claude"""
        self.logger.info(f"Analyzing question with Claude: {question[:50]}...")
        
        # Try Claude API first
        claude_response = self._call_claude_api(question)
        if claude_response:
            return {
                "answer": claude_response.answer,
                "confidence": claude_response.confidence,
                "source": claude_response.source,
                "model_version": claude_response.model_version,
                "tokens_used": claude_response.tokens_used,
                "success": True
            }
        
        # Fallback to knowledge base
        return self._fallback_response(question)
    
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when Claude API fails"""
        return {
            "answer": """🤖 **Claude AI không khả dụng**

Hiện tại Claude API đang gặp sự cố và không thể trả lời câu hỏi của bạn.

**Có thể do:**
- Claude API key không hợp lệ hoặc hết hạn
- Credit balance quá thấp
- Network connection issues
- Claude service đang bảo trì

**Cách khắc phục:**
1. Kiểm tra ANTHROPIC_API_KEY trong .env file
2. Kiểm tra credit balance tại https://console.anthropic.com/
3. Thử lại sau vài phút
4. Liên hệ support nếu vấn đề vẫn tiếp tục

💡 **Lưu ý**: Hãy thử lại sau khi Claude API hoạt động bình thường.""",
            "confidence": 0.0,
            "source": "fallback",
            "model_version": "local",
            "tokens_used": 0,
            "success": False
        }
    
    def explain_indicator(self, indicator: str) -> Dict:
        """Explain technical indicator in detail"""
        indicator_upper = indicator.upper()
        
        if indicator_upper in self.financial_knowledge["technical_indicators"]:
            explanation = self.financial_knowledge["technical_indicators"][indicator_upper]
            return {
                "answer": f"📊 **{indicator_upper} - Chỉ báo kỹ thuật**\n\n{explanation}\n\n🔍 **Cách sử dụng**:\n• Kết hợp với các chỉ báo khác\n• Xác nhận tín hiệu với khối lượng\n• Không nên dựa vào một chỉ báo duy nhất\n\n💡 **Lưu ý**: Chỉ báo kỹ thuật chỉ là công cụ hỗ trợ, không phải dự báo chính xác 100%.",
                "confidence": 0.9,
                "source": "knowledge_base",
                "model_version": "local",
                "tokens_used": 0,
                "success": True
            }
        
        # Try Claude API for unknown indicators
        return self.analyze_question(f"Giải thích chi tiết về chỉ báo kỹ thuật {indicator}")
    
    def get_investment_tips(self, topic: str = "general") -> List[str]:
        """Get investment tips based on topic"""
        tips = {
            "general": [
                "💡 Đa dạng hóa danh mục đầu tư để giảm rủi ro",
                "📊 Theo dõi chỉ số VN-Index và các chỉ báo kỹ thuật",
                "⏰ Đầu tư dài hạn thay vì lướt sóng ngắn hạn",
                "💰 Chỉ đầu tư số tiền có thể chấp nhận mất",
                "📈 Đặt stop loss để bảo vệ vốn",
                "📰 Cập nhật tin tức thị trường thường xuyên"
            ],
            "beginner": [
                "🎯 Bắt đầu với cổ phiếu blue-chip ổn định",
                "📚 Học kiến thức cơ bản về đầu tư",
                "💼 Mở tài khoản chứng khoán tại công ty uy tín",
                "📊 Tập trung vào phân tích cơ bản trước",
                "⏳ Kiên nhẫn, không vội vàng",
                "🤝 Tham gia cộng đồng đầu tư để học hỏi"
            ],
            "technical": [
                "📈 Sử dụng nhiều chỉ báo kỹ thuật kết hợp",
                "📊 RSI, MACD, Bollinger Bands là những chỉ báo cơ bản",
                "📉 Phân tích khối lượng giao dịch",
                "🎯 Xác định xu hướng trước khi vào lệnh",
                "⚠️ Không bỏ qua phân tích cơ bản",
                "📱 Sử dụng phần mềm phân tích chuyên nghiệp"
            ],
            "risk": [
                "⚠️ Luôn đặt stop loss cho mọi giao dịch",
                "📊 Tính toán tỷ lệ risk/reward trước khi vào lệnh",
                "💼 Không đặt quá 5% vốn vào một cổ phiếu",
                "📈 Theo dõi biến động thị trường",
                "🔄 Điều chỉnh danh mục định kỳ",
                "📰 Cập nhật tin tức rủi ro thị trường"
            ]
        }
        
        return tips.get(topic.lower(), tips["general"])
    
    def format_response(self, analysis: Dict) -> str:
        """Format analysis response for Telegram"""
        answer = analysis.get("answer", "")
        confidence = analysis.get("confidence", 0)
        source = analysis.get("source", "unknown")
        model_version = analysis.get("model_version", "unknown")
        tokens_used = analysis.get("tokens_used", 0)
        
        # Add metadata if available
        metadata = ""
        if source == "claude_api" and tokens_used > 0:
            metadata = f"\n\n---\n🤖 **Claude AI** | Độ tin cậy: {confidence:.1%} | Tokens: {tokens_used}"
        elif source == "fallback":
            metadata = f"\n\n---\n📚 **Claude API Error** | Độ tin cậy: {confidence:.1%}"
        
        return answer + metadata 