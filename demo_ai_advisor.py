"""
Demo AI Investment Advisor
Demo AI chuyên gia tư vấn đầu tư
"""

import sys
import os
sys.path.append('src')

from src.data.vn_alternative_collector import VNAlternativeCollector
from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.risk.risk_manager import RiskManager
from src.ai.investment_advisor import AIInvestmentAdvisor

def demo_ai_advisor():
    """Demo AI Investment Advisor"""
    print("🤖 AI Investment Advisor Demo")
    print("="*60)
    
    # Initialize components
    vn_collector = VNAlternativeCollector()
    us_collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    risk_manager = RiskManager()
    ai_advisor = AIInvestmentAdvisor()
    
    # Test symbols
    test_symbols = [
        ("VNM", "VN"),
        ("TCB", "VN"), 
        ("AAPL", "US"),
        ("MSFT", "US")
    ]
    
    for symbol, market in test_symbols:
        print(f"\n{'='*50}")
        print(f"📊 Phân tích {symbol} ({market})")
        print(f"{'='*50}")
        
        try:
            # Get data
            if market == "VN":
                data = vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
                if data.empty:
                    print(f"❌ Không thể lấy dữ liệu cho {symbol}")
                    continue
            else:
                data = us_collector.get_stock_data(symbol, period="6mo")
                if data.empty:
                    print(f"❌ Không thể lấy dữ liệu cho {symbol}")
                    continue
            
            current_price = data['Close'].iloc[-1]
            change = data['Returns'].iloc[-1] * 100
            
            print(f"💰 Giá hiện tại: {current_price:,.0f} {'VND' if market == 'VN' else 'USD'}")
            print(f"📈 Thay đổi: {change:+.2f}%")
            
            # Technical analysis
            data_with_indicators = analyzer.add_all_indicators(data)
            signals = analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = risk_manager.generate_risk_report(data, symbol)
            
            # AI recommendation
            recommendation = ai_advisor.generate_recommendation(
                symbol, data, signals, risk_report, market
            )
            
            # Investment strategy
            strategy = ai_advisor.get_investment_strategy(recommendation)
            
            # Display results
            print(f"\n🎯 **Khuyến nghị AI:** {recommendation.recommendation}")
            print(f"📊 **Độ tin cậy:** {recommendation.confidence:.1%}")
            print(f"⏰ **Khung thời gian:** {recommendation.time_horizon}")
            print(f"⚠️ **Mức rủi ro:** {recommendation.risk_level}")
            print(f"📈 **Tâm lý thị trường:** {recommendation.market_sentiment}")
            
            # Technical signals
            if 'error' not in signals:
                print(f"\n🎯 **Tín hiệu kỹ thuật:**")
                overall = signals.get('OVERALL', 'NEUTRAL')
                print(f"   Tổng thể: {overall}")
                
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        print(f"   {emoji} {indicator}: {signal}")
            
            # Risk metrics
            if 'error' not in risk_report:
                print(f"\n⚠️ **Chỉ số rủi ro:**")
                print(f"   Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}")
                print(f"   Max Drawdown: {risk_report['max_drawdown']:.2%}")
                print(f"   Total Return: {risk_report['total_return']:.2f}%")
                print(f"   VaR (95%): {risk_report['var_95']:.2%}")
            
            # AI reasoning
            if recommendation.reasoning:
                print(f"\n🧠 **Lý do AI đưa ra khuyến nghị:**")
                for i, reason in enumerate(recommendation.reasoning[:5], 1):
                    print(f"   {i}. {reason}")
            
            # Investment strategy
            print(f"\n📋 **Chiến lược đầu tư:**")
            print(f"   Hành động: {strategy['action']}")
            print(f"   Kích thước vị thế: {strategy['position_size']}")
            print(f"   Vào lệnh: {strategy['entry_strategy']}")
            print(f"   Thoát lệnh: {strategy['exit_strategy']}")
            print(f"   Quản lý rủi ro: {strategy['risk_management']}")
            
            # Target price and stop loss
            if recommendation.target_price and recommendation.stop_loss:
                currency = "VND" if market == "VN" else "USD"
                print(f"\n💰 **Mục tiêu giá:** {recommendation.target_price:,.0f} {currency}")
                print(f"🛑 **Stop Loss:** {recommendation.stop_loss:,.0f} {currency}")
            
        except Exception as e:
            print(f"❌ Lỗi khi phân tích {symbol}: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🎉 Demo AI Investment Advisor hoàn thành!")
    print("="*60)
    print("\nĐể sử dụng AI Advisor trong Telegram Bot:")
    print("   /stock VNM - Phân tích với AI")
    print("   /stock AAPL - Phân tích với AI")

if __name__ == "__main__":
    demo_ai_advisor() 