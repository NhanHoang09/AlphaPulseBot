"""
FinGPT Demo
Demo các tính năng của bot phân tích tài chính
"""

import sys
import os
import logging
from datetime import datetime

# Add src to path
sys.path.append('src')

from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def demo_data_collection():
    """Demo thu thập dữ liệu"""
    print("\n" + "="*50)
    print("📊 DEMO: Thu thập dữ liệu")
    print("="*50)
    
    collector = DataCollector()
    
    # Test stock data
    print("🔍 Lấy dữ liệu Apple (AAPL)...")
    apple_data = collector.get_stock_data("AAPL", period="6mo")
    if not apple_data.empty:
        print(f"✅ Đã lấy {len(apple_data)} điểm dữ liệu cho AAPL")
        print(f"   Giá hiện tại: ${apple_data['Close'].iloc[-1]:.2f}")
        print(f"   Khoảng thời gian: {apple_data.index[0].strftime('%Y-%m-%d')} đến {apple_data.index[-1].strftime('%Y-%m-%d')}")
    else:
        print("❌ Không thể lấy dữ liệu AAPL")
    
    # Test crypto data
    print("\n🔍 Lấy dữ liệu Bitcoin (BTC-USD)...")
    btc_data = collector.get_crypto_data("BTC-USD", period="1mo")
    if not btc_data.empty:
        print(f"✅ Đã lấy {len(btc_data)} điểm dữ liệu cho BTC")
        print(f"   Giá hiện tại: ${btc_data['Close'].iloc[-1]:.2f}")
    else:
        print("❌ Không thể lấy dữ liệu BTC")

def demo_technical_analysis():
    """Demo phân tích kỹ thuật"""
    print("\n" + "="*50)
    print("📈 DEMO: Phân tích kỹ thuật")
    print("="*50)
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    
    # Get data
    data = collector.get_stock_data("MSFT", period="6mo")
    if data.empty:
        print("❌ Không thể lấy dữ liệu MSFT")
        return
    
    # Add technical indicators
    print("🔧 Thêm các chỉ báo kỹ thuật...")
    data_with_indicators = analyzer.add_all_indicators(data)
    
    # Get trading signals
    print("🎯 Phân tích tín hiệu giao dịch...")
    signals = analyzer.get_trading_signals(data_with_indicators)
    
    if 'error' not in signals:
        print("✅ Tín hiệu giao dịch:")
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
    patterns = analyzer.detect_patterns(data)
    if patterns:
        print(f"✅ Phát hiện {len(patterns)} mô hình:")
        for pattern in patterns[-3:]:  # Show last 3
            print(f"   📊 {pattern['pattern']} - {pattern['signal']} ({pattern['strength']})")
    else:
        print("ℹ️ Không phát hiện mô hình đặc biệt")

def demo_ai_prediction():
    """Demo dự báo AI"""
    print("\n" + "="*50)
    print("🤖 DEMO: Dự báo AI")
    print("="*50)
    
    collector = DataCollector()
    predictor = PredictionModels()
    
    # Get data
    data = collector.get_stock_data("GOOGL", period="1y")
    if data.empty:
        print("❌ Không thể lấy dữ liệu GOOGL")
        return
    
    # Train LSTM model
    print("🚀 Training LSTM model...")
    lstm_result = predictor.train_lstm_model(data, "GOOGL", epochs=10)  # Reduced epochs for demo
    
    if 'error' not in lstm_result:
        print("✅ LSTM model training thành công!")
        print(f"   MSE: {lstm_result['mse']:.6f}")
        print(f"   MAE: {lstm_result['mae']:.6f}")
        print(f"   R²: {lstm_result['r2']:.4f}")
        
        # Make prediction
        print("\n🔮 Tạo dự báo...")
        prediction = predictor.predict(data, "GOOGL", "lstm")
        
        if 'error' not in prediction:
            current_price = prediction['current_price']
            predicted_price = prediction['predicted_price']
            change = ((predicted_price - current_price) / current_price) * 100
            
            print("✅ Dự báo:")
            print(f"   Giá hiện tại: ${current_price:.2f}")
            print(f"   Giá dự báo: ${predicted_price:.2f}")
            print(f"   Thay đổi dự kiến: {change:+.2f}%")
        else:
            print(f"❌ Lỗi dự báo: {prediction['error']}")
    else:
        print(f"❌ Lỗi training: {lstm_result['error']}")

def demo_risk_management():
    """Demo quản lý rủi ro"""
    print("\n" + "="*50)
    print("⚠️ DEMO: Quản lý rủi ro")
    print("="*50)
    
    collector = DataCollector()
    risk_manager = RiskManager()
    
    # Get data
    data = collector.get_stock_data("TSLA", period="1y")
    if data.empty:
        print("❌ Không thể lấy dữ liệu TSLA")
        return
    
    # Generate risk report
    print("📊 Tạo báo cáo rủi ro...")
    risk_report = risk_manager.generate_risk_report(data, "TSLA")
    
    if 'error' not in risk_report:
        print("✅ Báo cáo rủi ro:")
        print(f"   Volatility: {risk_report['volatility_annual']:.2%}")
        print(f"   VaR (95%): {risk_report['var_95']:.2%}")
        print(f"   Sharpe Ratio: {risk_report['sharpe_ratio']:.2f}")
        print(f"   Max Drawdown: {risk_report['max_drawdown']:.2%}")
        print(f"   Total Return: {risk_report['total_return']:.2f}%")
    else:
        print(f"❌ Lỗi: {risk_report['error']}")
    
    # Risk alerts
    print("\n🚨 Kiểm tra cảnh báo rủi ro...")
    alerts = risk_manager.get_risk_alerts(data, "TSLA")
    
    if alerts:
        print("⚠️ Cảnh báo rủi ro:")
        for alert in alerts:
            severity_emoji = "🚨" if alert['severity'] == 'CRITICAL' else "⚠️"
            print(f"   {severity_emoji} {alert['message']}")
    else:
        print("✅ Không có cảnh báo rủi ro")

def demo_portfolio_optimization():
    """Demo tối ưu hóa portfolio"""
    print("\n" + "="*50)
    print("📊 DEMO: Tối ưu hóa Portfolio")
    print("="*50)
    
    collector = DataCollector()
    risk_manager = RiskManager()
    
    # Get data for multiple symbols
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    returns_data = {}
    
    print("📈 Thu thập dữ liệu cho portfolio...")
    for symbol in symbols:
        data = collector.get_stock_data(symbol, period="1y")
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
        print("\n🔍 Tối ưu hóa portfolio...")
        portfolio = risk_manager.optimize_portfolio(returns_df, 'sharpe')
        
        print("✅ Kết quả tối ưu hóa:")
        print(f"   Expected Return: {portfolio['portfolio_return']:.2%}")
        print(f"   Volatility: {portfolio['portfolio_volatility']:.2%}")
        print(f"   Sharpe Ratio: {portfolio['sharpe_ratio']:.2f}")
        
        print("\n📊 Portfolio Weights:")
        for asset, weight in portfolio['weights'].items():
            print(f"   {asset}: {weight:.2%}")
    else:
        print("❌ Không đủ dữ liệu để tối ưu hóa portfolio")

def main():
    """Main demo function"""
    print("🤖 FinGPT - AI Trading Bot Demo")
    print("="*60)
    print("Demo các tính năng chính của bot phân tích tài chính")
    print("="*60)
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    try:
        # Run demos
        demo_data_collection()
        demo_technical_analysis()
        demo_ai_prediction()
        demo_risk_management()
        demo_portfolio_optimization()
        
        print("\n" + "="*60)
        print("🎉 Demo hoàn thành!")
        print("="*60)
        print("\nĐể chạy web dashboard:")
        print("   streamlit run src/ui/dashboard.py")
        print("\nĐể chạy bot tự động:")
        print("   python src/main.py")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong demo: {str(e)}")
        logging.error(f"Demo error: {str(e)}")

if __name__ == "__main__":
    main() 