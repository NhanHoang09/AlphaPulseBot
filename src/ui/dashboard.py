"""
FinGPT Dashboard
Giao diện web cho bot phân tích tài chính
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager

# Page config
st.set_page_config(
    page_title="FinGPT - AI Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class FinGPTDashboard:
    """Main dashboard class"""
    
    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.predictor = PredictionModels()
        self.risk_manager = RiskManager()
        
        # Initialize session state
        if 'data' not in st.session_state:
            st.session_state.data = {}
        if 'analysis' not in st.session_state:
            st.session_state.analysis = {}
        if 'predictions' not in st.session_state:
            st.session_state.predictions = {}
    
    def main_header(self):
        """Main header"""
        st.markdown('<h1 class="main-header">🤖 FinGPT - AI Trading Bot</h1>', unsafe_allow_html=True)
        st.markdown("### Phân tích và dự báo xu hướng thị trường với AI")
    
    def sidebar(self):
        """Sidebar configuration"""
        st.sidebar.title("⚙️ Cấu hình")
        
        # Symbol input
        symbol = st.sidebar.text_input("Mã cổ phiếu", value="AAPL").upper()
        
        # Time period
        period = st.sidebar.selectbox(
            "Khoảng thời gian",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3
        )
        
        # Analysis type
        analysis_type = st.sidebar.selectbox(
            "Loại phân tích",
            ["Technical Analysis", "AI Prediction", "Risk Analysis", "Portfolio Optimization"]
        )
        
        # Update button
        if st.sidebar.button("🔄 Cập nhật dữ liệu"):
            with st.spinner("Đang tải dữ liệu..."):
                data = self.collector.get_stock_data(symbol, period=period)
                if not data.empty:
                    st.session_state.data[symbol] = data
                    st.success(f"Đã tải dữ liệu cho {symbol}")
                else:
                    st.error(f"Không thể tải dữ liệu cho {symbol}")
        
        return symbol, period, analysis_type
    
    def display_price_chart(self, data: pd.DataFrame, symbol: str):
        """Hiển thị biểu đồ giá"""
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{symbol} Price Chart', 'Volume', 'RSI'),
            row_width=[0.6, 0.2, 0.2]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )
        
        # Moving averages
        if 'SMA_20' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='orange')),
                row=1, col=1
            )
        
        if 'SMA_50' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='blue')),
                row=1, col=1
            )
        
        # Bollinger Bands
        if 'BB_Upper' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dash')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=data.index, y=data['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dash'), fill='tonexty'),
                row=1, col=1
            )
        
        # Volume
        colors = ['red' if close < open else 'green' for close, open in zip(data['Close'], data['Open'])]
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors),
            row=2, col=1
        )
        
        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')),
                row=3, col=1
            )
            # Overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        fig.update_layout(
            title=f'{symbol} Technical Analysis',
            xaxis_rangeslider_visible=False,
            height=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_technical_analysis(self, data: pd.DataFrame, symbol: str):
        """Hiển thị phân tích kỹ thuật"""
        st.subheader("📊 Phân tích kỹ thuật")
        
        # Add technical indicators
        data_with_indicators = self.analyzer.add_all_indicators(data)
        
        # Display price chart
        self.display_price_chart(data_with_indicators, symbol)
        
        # Trading signals
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 Tín hiệu giao dịch")
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            if 'error' not in signals:
                for indicator, signal in signals.items():
                    if indicator != 'OVERALL':
                        color = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
                        st.write(f"{color} {indicator}: {signal}")
                
                # Overall signal
                overall = signals.get('OVERALL', 'NEUTRAL')
                if overall == 'BUY':
                    st.success(f"🎯 Tín hiệu tổng thể: {overall}")
                elif overall == 'SELL':
                    st.error(f"🎯 Tín hiệu tổng thể: {overall}")
                else:
                    st.warning(f"🎯 Tín hiệu tổng thể: {overall}")
        
        with col2:
            st.subheader("📈 Chỉ số kỹ thuật")
            latest = data_with_indicators.iloc[-1]
            
            metrics = {
                'RSI': f"{latest.get('RSI', 0):.2f}",
                'MACD': f"{latest.get('MACD', 0):.4f}",
                'BB Position': f"{latest.get('BB_Position', 0):.2f}",
                'ATR': f"{latest.get('ATR', 0):.2f}"
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
        
        with col3:
            st.subheader("🎨 Mô hình giá")
            patterns = self.analyzer.detect_patterns(data)
            
            if patterns:
                for pattern in patterns[-3:]:  # Show last 3 patterns
                    st.write(f"📊 {pattern['pattern']} - {pattern['signal']}")
            else:
                st.write("Không phát hiện mô hình đặc biệt")
    
    def display_ai_prediction(self, data: pd.DataFrame, symbol: str):
        """Hiển thị dự báo AI"""
        st.subheader("🤖 Dự báo AI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Training Model")
            
            model_type = st.selectbox("Loại model", ["LSTM", "Ensemble"])
            
            if st.button("🚀 Training Model"):
                with st.spinner("Đang training model..."):
                    if model_type == "LSTM":
                        result = self.predictor.train_lstm_model(data, symbol)
                    else:
                        result = self.predictor.train_ensemble_model(data, symbol)
                    
                    if 'error' not in result:
                        st.success("Training thành công!")
                        st.json(result)
                    else:
                        st.error(f"Lỗi training: {result['error']}")
        
        with col2:
            st.subheader("🔮 Dự báo")
            
            if st.button("🔮 Tạo dự báo"):
                with st.spinner("Đang tạo dự báo..."):
                    prediction = self.predictor.predict(data, symbol, model_type.lower())
                    
                    if 'error' not in prediction:
                        current_price = prediction['current_price']
                        predicted_price = prediction['predicted_price']
                        
                        st.metric("Giá hiện tại", f"${current_price:.2f}")
                        st.metric("Giá dự báo", f"${predicted_price:.2f}")
                        
                        change = ((predicted_price - current_price) / current_price) * 100
                        st.metric("Thay đổi dự kiến", f"{change:+.2f}%")
                        
                        # Prediction chart
                        dates = pd.date_range(start=data.index[-1], periods=7, freq='D')
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=data.index[-30:],
                            y=data['Close'][-30:],
                            name='Historical',
                            line=dict(color='blue')
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=dates,
                            y=[current_price] + [predicted_price] * 6,
                            name='Prediction',
                            line=dict(color='red', dash='dash')
                        ))
                        
                        fig.update_layout(title=f'{symbol} Price Prediction')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"Lỗi dự báo: {prediction['error']}")
    
    def display_risk_analysis(self, data: pd.DataFrame, symbol: str):
        """Hiển thị phân tích rủi ro"""
        st.subheader("⚠️ Phân tích rủi ro")
        
        # Generate risk report
        risk_report = self.risk_manager.generate_risk_report(data, symbol)
        
        if 'error' not in risk_report:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Volatility", f"{risk_report['volatility_annual']:.2%}")
                st.metric("Sharpe Ratio", f"{risk_report['sharpe_ratio']:.2f}")
            
            with col2:
                st.metric("VaR (95%)", f"{risk_report['var_95']:.2%}")
                st.metric("Sortino Ratio", f"{risk_report['sortino_ratio']:.2f}")
            
            with col3:
                st.metric("Max Drawdown", f"{risk_report['max_drawdown']:.2%}")
                st.metric("Total Return", f"{risk_report['total_return']:.2f}%")
            
            with col4:
                st.metric("Current Price", f"${risk_report['current_price']:.2f}")
                st.metric("CVaR (95%)", f"{risk_report['cvar_95']:.2%}")
            
            # Risk alerts
            st.subheader("🚨 Cảnh báo rủi ro")
            alerts = self.risk_manager.get_risk_alerts(data, symbol)
            
            if alerts:
                for alert in alerts:
                    if alert['severity'] == 'CRITICAL':
                        st.markdown(f'<div class="alert-danger">🚨 {alert["message"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="alert-warning">⚠️ {alert["message"]}</div>', unsafe_allow_html=True)
            else:
                st.success("✅ Không có cảnh báo rủi ro")
            
            # Risk metrics chart
            returns = self.risk_manager.calculate_returns(data['Close'])
            volatility = self.risk_manager.calculate_volatility(returns)
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Returns', 'Volatility'),
                vertical_spacing=0.1
            )
            
            fig.add_trace(
                go.Scatter(x=returns.index, y=returns, name='Returns', line=dict(color='blue')),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=volatility.index, y=volatility, name='Volatility', line=dict(color='red')),
                row=2, col=1
            )
            
            fig.update_layout(height=600, title_text=f"{symbol} Risk Metrics")
            st.plotly_chart(fig, use_container_width=True)
    
    def display_portfolio_optimization(self):
        """Hiển thị tối ưu hóa portfolio"""
        st.subheader("📊 Tối ưu hóa Portfolio")
        
        # Input symbols
        symbols_input = st.text_input("Nhập các mã cổ phiếu (phân cách bằng dấu phẩy)", "AAPL,MSFT,GOOGL,AMZN")
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        
        if st.button("🔍 Phân tích Portfolio"):
            with st.spinner("Đang phân tích portfolio..."):
                returns_data = pd.DataFrame()
                
                for symbol in symbols:
                    data = self.collector.get_stock_data(symbol, period="1y")
                    if not data.empty:
                        returns_data[symbol] = self.risk_manager.calculate_returns(data['Close'])
                
                if len(returns_data.columns) > 1:
                    # Portfolio optimization
                    portfolio = self.risk_manager.optimize_portfolio(returns_data, 'sharpe')
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Portfolio Weights")
                        weights_df = pd.DataFrame(list(portfolio['weights'].items()), columns=['Asset', 'Weight'])
                        st.bar_chart(weights_df.set_index('Asset'))
                    
                    with col2:
                        st.subheader("📊 Portfolio Metrics")
                        st.metric("Expected Return", f"{portfolio['portfolio_return']:.2%}")
                        st.metric("Volatility", f"{portfolio['portfolio_volatility']:.2%}")
                        st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.2f}")
                    
                    # Correlation matrix
                    st.subheader("🔗 Correlation Matrix")
                    corr_matrix = self.risk_manager.calculate_correlation_matrix(returns_data)
                    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Không đủ dữ liệu để phân tích portfolio")
    
    def run(self):
        """Chạy dashboard"""
        self.main_header()
        
        # Sidebar
        symbol, period, analysis_type = self.sidebar()
        
        # Main content
        if symbol and symbol in st.session_state.data:
            data = st.session_state.data[symbol]
            
            # Display current info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Giá hiện tại", f"${data['Close'].iloc[-1]:.2f}")
            with col2:
                daily_return = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                st.metric("Thay đổi hôm nay", f"{daily_return:+.2f}%")
            with col3:
                st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
            with col4:
                st.metric("Cập nhật lần cuối", data.index[-1].strftime("%Y-%m-%d"))
            
            # Analysis type
            if analysis_type == "Technical Analysis":
                self.display_technical_analysis(data, symbol)
            elif analysis_type == "AI Prediction":
                self.display_ai_prediction(data, symbol)
            elif analysis_type == "Risk Analysis":
                self.display_risk_analysis(data, symbol)
            elif analysis_type == "Portfolio Optimization":
                self.display_portfolio_optimization()
        
        else:
            st.info("👈 Vui lòng nhập mã cổ phiếu và nhấn 'Cập nhật dữ liệu' để bắt đầu")
            
            # Sample data for demonstration
            if st.button("🎯 Xem demo với AAPL"):
                with st.spinner("Đang tải dữ liệu demo..."):
                    data = self.collector.get_stock_data("AAPL", period="6mo")
                    if not data.empty:
                        st.session_state.data["AAPL"] = data
                        st.success("Đã tải dữ liệu demo cho AAPL")
                        st.rerun()

if __name__ == "__main__":
    dashboard = FinGPTDashboard()
    dashboard.run() 