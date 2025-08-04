"""
Quick Vietnam Market Demo
Demo nhanh cho thị trường chứng khoán Việt Nam
"""

import sys
import os
sys.path.append('src')

from src.data.vn_alternative_collector import VNAlternativeCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.risk.risk_manager import RiskManager

def quick_vn_demo():
    """Demo nhanh cho thị trường VN"""
    print("🇻🇳 FinGPT - Quick Vietnam Market Demo")
    print("="*50)
    
    # Khởi tạo collectors
    vn_collector = VNAlternativeCollector()
    analyzer = TechnicalAnalyzer()
    risk_manager = RiskManager()
    
    # Lấy dữ liệu VNM
    print("📊 Lấy dữ liệu VNM (Vinamilk)...")
    vnm_data = vn_collector.get_vn_stock_data_yahoo("VNM", period="6mo")
    
    if vnm_data.empty:
        print("🔧 Sử dụng dữ liệu mẫu...")
        sample_data = vn_collector.get_sample_vn_data()
        vnm_data = sample_data['VNM']
    
    print(f"✅ VNM: {vnm_data['Close'].iloc[-1]:,.0f} VND")
    print(f"   Thay đổi: {vnm_data['Returns'].iloc[-1]*100:.2f}%")
    
    # Phân tích kỹ thuật
    print("\n📈 Phân tích kỹ thuật...")
    data_with_indicators = analyzer.add_all_indicators(vnm_data)
    signals = analyzer.get_trading_signals(data_with_indicators)
    
    if 'error' not in signals:
        overall = signals.get('OVERALL', 'NEUTRAL')
        print(f"🎯 Tín hiệu: {overall}")
        
        for indicator, signal in signals.items():
            if indicator != 'OVERALL':
                emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                print(f"   {emoji} {indicator}: {signal}")
    
    # Quản lý rủi ro
    print("\n⚠️ Quản lý rủi ro...")
    risk_report = risk_manager.generate_risk_report(vnm_data, "VNM")
    
    if 'error' not in risk_report:
        print(f"📊 Volatility: {risk_report['volatility_annual']:.2%}")
        print(f"📊 Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}")
        print(f"📊 Max Drawdown: {risk_report['max_drawdown']:.2%}")
        print(f"📊 Total Return: {risk_report['total_return']:.2f}%")
    
    # Portfolio optimization
    print("\n📊 Tối ưu hóa portfolio...")
    symbols = ["VNM", "TCB", "HPG"]
    returns_data = {}
    
    for symbol in symbols:
        data = vn_collector.get_vn_stock_data_yahoo(symbol, period="1y")
        if data.empty:
            sample_data = vn_collector.get_sample_vn_data()
            if symbol in sample_data:
                data = sample_data[symbol]
        
        if not data.empty:
            returns_data[symbol] = risk_manager.calculate_returns(data['Close'])
    
    if len(returns_data) > 1:
        import pandas as pd
        returns_df = pd.DataFrame(returns_data)
        portfolio = risk_manager.optimize_portfolio(returns_df, 'sharpe')
        
        print(f"📈 Expected Return: {portfolio['portfolio_return']:.2%}")
        print(f"📈 Sharpe Ratio: {portfolio['sharpe_ratio']:.2f}")
        
        print("📊 Weights:")
        for asset, weight in portfolio['weights'].items():
            print(f"   {asset}: {weight:.1%}")
    
    print("\n🎉 Demo hoàn thành!")
    print("\nĐể chạy web dashboard:")
    print("   streamlit run src/ui/dashboard.py")

if __name__ == "__main__":
    quick_vn_demo() 