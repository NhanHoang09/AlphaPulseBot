"""
FinGPT Vietnam Market Demo
Demo các tính năng của bot phân tích tài chính cho thị trường VN
"""

import sys
import os
import logging
from datetime import datetime

# Add src to path
sys.path.append('src')

from src.data.vn_alternative_collector import VNAlternativeCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def demo_vn_data_collection():
    """Demo thu thập dữ liệu thị trường VN"""
    print("\n" + "="*50)
    print("📊 DEMO: Thu thập dữ liệu thị trường VN")
    print("="*50)
    
    vn_collector = VNAlternativeCollector()
    
    # Test lấy dữ liệu VNM (Vinamilk)
    print("🔍 Lấy dữ liệu VNM (Vinamilk)...")
    vnm_data = vn_collector.get_vn_stock_data_yahoo("VNM", period="6mo")
    if vnm_data.empty:
        print("🔧 Sử dụng dữ liệu mẫu cho VNM...")
        sample_data = vn_collector.get_sample_vn_data()
        vnm_data = sample_data['VNM']
    if not vnm_data.empty:
        print(f"✅ Đã lấy {len(vnm_data)} điểm dữ liệu cho VNM")
        print(f"   Giá hiện tại: {vnm_data['Close'].iloc[-1]:,.0f} VND")
        print(f"   Thay đổi: {vnm_data['Returns'].iloc[-1]*100:.2f}%")
        print(f"   Khoảng thời gian: {vnm_data.index[0].strftime('%Y-%m-%d')} đến {vnm_data.index[-1].strftime('%Y-%m-%d')}")
    else:
        print("❌ Không thể lấy dữ liệu VNM")
    
    # Test lấy dữ liệu TCB (Techcombank)
    print("\n🔍 Lấy dữ liệu TCB (Techcombank)...")
    tcb_data = vn_collector.get_vn_stock_data_yahoo("TCB", period="3mo")
    if tcb_data.empty:
        print("🔧 Sử dụng dữ liệu mẫu cho TCB...")
        sample_data = vn_collector.get_sample_vn_data()
        tcb_data = sample_data['TCB']
    if not tcb_data.empty:
        print(f"✅ Đã lấy {len(tcb_data)} điểm dữ liệu cho TCB")
        print(f"   Giá hiện tại: {tcb_data['Close'].iloc[-1]:,.0f} VND")
        print(f"   Thay đổi: {tcb_data['Returns'].iloc[-1]*100:.2f}%")
    else:
        print("❌ Không thể lấy dữ liệu TCB")
    
    # Test lấy VNINDEX
    print("\n🔍 Lấy dữ liệu VNINDEX...")
    vnindex_data = vn_collector.get_vn_index_data_yahoo("VNINDEX", period="1mo")
    if vnindex_data.empty:
        print("🔧 Sử dụng dữ liệu mẫu cho VNINDEX...")
        sample_data = vn_collector.get_sample_vn_data()
        vnindex_data = sample_data['VNINDEX']
    if not vnindex_data.empty:
        print(f"✅ Đã lấy {len(vnindex_data)} điểm dữ liệu cho VNINDEX")
        print(f"   Giá hiện tại: {vnindex_data['Close'].iloc[-1]:,.2f}")
        print(f"   Thay đổi: {vnindex_data['Returns'].iloc[-1]*100:.2f}%")
    else:
        print("❌ Không thể lấy dữ liệu VNINDEX")
    
    return vnm_data, tcb_data, vnindex_data

def demo_vn_technical_analysis(vnm_data):
    """Demo phân tích kỹ thuật cho VN"""
    print("\n" + "="*50)
    print("📈 DEMO: Phân tích kỹ thuật thị trường VN")
    print("="*50)
    
    if vnm_data.empty:
        print("❌ Không có dữ liệu để phân tích")
        return
    
    analyzer = TechnicalAnalyzer()
    
    # Add technical indicators
    print("🔧 Thêm các chỉ báo kỹ thuật...")
    data_with_indicators = analyzer.add_all_indicators(vnm_data)
    
    # Get trading signals
    print("🎯 Phân tích tín hiệu giao dịch...")
    signals = analyzer.get_trading_signals(data_with_indicators)
    
    if 'error' not in signals:
        print("✅ Tín hiệu giao dịch cho VNM:")
        for indicator, signal in signals.items():
            if indicator != 'OVERALL':
                emoji = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                print(f"   {emoji} {indicator}: {signal}")
        
        overall = signals.get('OVERALL', 'NEUTRAL')
        print(f"\n🎯 Tín hiệu tổng thể: {overall}")
    else:
        print(f"❌ Lỗi: {signals['error']}")
    
    # Detect patterns
    print("\n🎨 Phát hiện mô hình giá...")
    patterns = analyzer.detect_patterns(vnm_data)
    if patterns:
        print(f"✅ Phát hiện {len(patterns)} mô hình:")
        for pattern in patterns[-3:]:  # Show last 3
            print(f"   📊 {pattern['pattern']} - {pattern['signal']} ({pattern['strength']})")
    else:
        print("ℹ️ Không phát hiện mô hình đặc biệt")

def demo_vn_ai_prediction(vnm_data):
    """Demo dự báo AI cho VN"""
    print("\n" + "="*50)
    print("🤖 DEMO: Dự báo AI cho thị trường VN")
    print("="*50)
    
    if vnm_data.empty:
        print("❌ Không có dữ liệu để dự báo")
        return
    
    predictor = PredictionModels()
    
    # Train LSTM model
    print("🚀 Training LSTM model cho VNM...")
    lstm_result = predictor.train_lstm_model(vnm_data, "VNM", epochs=10)  # Reduced epochs for demo
    
    if 'error' not in lstm_result:
        print("✅ LSTM model training thành công!")
        print(f"   MSE: {lstm_result['mse']:.6f}")
        print(f"   MAE: {lstm_result['mae']:.6f}")
        print(f"   R²: {lstm_result['r2']:.4f}")
        
        # Make prediction
        print("\n🔮 Tạo dự báo...")
        prediction = predictor.predict(vnm_data, "VNM", "lstm")
        
        if 'error' not in prediction:
            current_price = prediction['current_price']
            predicted_price = prediction['predicted_price']
            change = ((predicted_price - current_price) / current_price) * 100
            
            print("✅ Dự báo cho VNM:")
            print(f"   Giá hiện tại: {current_price:,.0f} VND")
            print(f"   Giá dự báo: {predicted_price:,.0f} VND")
            print(f"   Thay đổi dự kiến: {change:+.2f}%")
        else:
            print(f"❌ Lỗi dự báo: {prediction['error']}")
    else:
        print(f"❌ Lỗi training: {lstm_result['error']}")

def demo_vn_risk_management(vnm_data):
    """Demo quản lý rủi ro cho VN"""
    print("\n" + "="*50)
    print("⚠️ DEMO: Quản lý rủi ro thị trường VN")
    print("="*50)
    
    if vnm_data.empty:
        print("❌ Không có dữ liệu để phân tích rủi ro")
        return
    
    risk_manager = RiskManager()
    
    # Generate risk report
    print("📊 Tạo báo cáo rủi ro cho VNM...")
    risk_report = risk_manager.generate_risk_report(vnm_data, "VNM")
    
    if 'error' not in risk_report:
        print("✅ Báo cáo rủi ro cho VNM:")
        print(f"   Volatility: {risk_report['volatility_annual']:.2%}")
        print(f"   VaR (95%): {risk_report['var_95']:.2%}")
        print(f"   Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}")
        print(f"   Max Drawdown: {risk_report['max_drawdown']:.2%}")
        print(f"   Total Return: {risk_report['total_return']:.2f}%")
    else:
        print(f"❌ Lỗi: {risk_report['error']}")
    
    # Risk alerts
    print("\n🚨 Kiểm tra cảnh báo rủi ro...")
    alerts = risk_manager.get_risk_alerts(vnm_data, "VNM")
    
    if alerts:
        print("⚠️ Cảnh báo rủi ro:")
        for alert in alerts:
            severity_emoji = "🚨" if alert['severity'] == 'CRITICAL' else "⚠️"
            print(f"   {severity_emoji} {alert['message']}")
    else:
        print("✅ Không có cảnh báo rủi ro")

def demo_vn_portfolio_optimization():
    """Demo tối ưu hóa portfolio VN"""
    print("\n" + "="*50)
    print("📊 DEMO: Tối ưu hóa Portfolio thị trường VN")
    print("="*50)
    
    vn_collector = VNAlternativeCollector()
    risk_manager = RiskManager()
    
    # Get data for multiple VN stocks
    symbols = ["VNM", "TCB", "HPG", "FPT"]
    returns_data = {}
    
    print("📈 Thu thập dữ liệu cho portfolio VN...")
    for symbol in symbols:
        data = vn_collector.get_vn_stock_data_yahoo(symbol, period="1y")
        if data.empty:
            print(f"   🔧 Sử dụng dữ liệu mẫu cho {symbol}...")
            sample_data = vn_collector.get_sample_vn_data()
            if symbol in sample_data:
                data = sample_data[symbol]
        if not data.empty:
            returns_data[symbol] = risk_manager.calculate_returns(data['Close'])
            print(f"   ✅ {symbol}: {len(returns_data[symbol])} điểm dữ liệu")
        else:
            print(f"   ❌ {symbol}: Không thể lấy dữ liệu")
    
    if len(returns_data) > 1:
        # Create DataFrame
        import pandas as pd
        returns_df = pd.DataFrame(returns_data)
        
        # Portfolio optimization
        print("\n🔍 Tối ưu hóa portfolio VN...")
        portfolio = risk_manager.optimize_portfolio(returns_df, 'sharpe')
        
        print("✅ Kết quả tối ưu hóa portfolio VN:")
        print(f"   Expected Return: {portfolio['portfolio_return']:.2%}")
        print(f"   Volatility: {portfolio['portfolio_volatility']:.2%}")
        print(f"   Sharpe Ratio: {portfolio['sharpe_ratio']:.2f}")
        
        print("\n📊 Portfolio Weights:")
        for asset, weight in portfolio['weights'].items():
            print(f"   {asset}: {weight:.2%}")
    else:
        print("❌ Không đủ dữ liệu để tối ưu hóa portfolio")

def demo_vn_market_summary():
    """Demo tổng quan thị trường VN"""
    print("\n" + "="*50)
    print("📈 DEMO: Tổng quan thị trường VN")
    print("="*50)
    
    vn_collector = VNAlternativeCollector()
    
    # Get market summary
    print("🔍 Lấy tổng quan thị trường...")
    summary = vn_collector.get_vn_market_summary()
    
    if summary:
        print("✅ Tổng quan thị trường VN:")
        print(f"   {summary['index']}: {summary['current_value']:,.2f}")
        print(f"   Thay đổi: {summary['change']:+.2f} ({summary['change_pct']:+.2f}%)")
        print(f"   Volume: {summary['volume']:,.0f}")
        print(f"   Ngày: {summary['date']}")
    else:
        print("❌ Không thể lấy tổng quan thị trường")

def main():
    """Main demo function"""
    print("🤖 FinGPT - Vietnam Market Demo")
    print("="*60)
    print("Demo các tính năng của bot phân tích tài chính cho thị trường VN")
    print("="*60)
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    try:
        # Run demos
        vnm_data, tcb_data, vnindex_data = demo_vn_data_collection()
        demo_vn_technical_analysis(vnm_data)
        demo_vn_ai_prediction(vnm_data)
        demo_vn_risk_management(vnm_data)
        demo_vn_portfolio_optimization()
        demo_vn_market_summary()
        
        print("\n" + "="*60)
        print("🎉 Demo thị trường VN hoàn thành!")
        print("="*60)
        print("\nĐể chạy web dashboard cho thị trường VN:")
        print("   streamlit run src/ui/dashboard.py")
        print("\nĐể chạy bot tự động cho thị trường VN:")
        print("   python src/main.py")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong demo VN: {str(e)}")
        logging.error(f"Demo VN error: {str(e)}")

if __name__ == "__main__":
    main() 