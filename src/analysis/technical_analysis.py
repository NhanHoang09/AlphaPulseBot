"""
Technical Analysis Module
Phân tích kỹ thuật với các chỉ báo phổ biến
"""

import pandas as pd
import numpy as np
import ta
# import pandas_ta as pta  # Commented out due to compatibility issues
from typing import Dict, List, Tuple, Optional
import logging

class TechnicalAnalyzer:
    """Class phân tích kỹ thuật"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_moving_averages(self, data: pd.DataFrame, windows: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """
        Thêm các đường trung bình động
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            windows: Danh sách các cửa sổ tính toán
        
        Returns:
            DataFrame với các đường MA
        """
        df = data.copy()
        
        for window in windows:
            df[f'SMA_{window}'] = ta.trend.sma_indicator(df['Close'], window=window)
            df[f'EMA_{window}'] = ta.trend.ema_indicator(df['Close'], window=window)
        
        return df
    
    def add_rsi(self, data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Thêm chỉ báo RSI (Relative Strength Index)
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            window: Cửa sổ tính toán RSI
        
        Returns:
            DataFrame với RSI
        """
        df = data.copy()
        df['RSI'] = ta.momentum.rsi(df['Close'], window=window)
        return df
    
    def add_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Thêm chỉ báo MACD
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            fast: EMA nhanh
            slow: EMA chậm
            signal: Signal line
        
        Returns:
            DataFrame với MACD
        """
        df = data.copy()
        
        macd = ta.trend.MACD(df['Close'], window_fast=fast, window_slow=slow, window_sign=signal)
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Histogram'] = macd.macd_diff()
        
        return df
    
    def add_bollinger_bands(self, data: pd.DataFrame, window: int = 20, std: int = 2) -> pd.DataFrame:
        """
        Thêm Bollinger Bands
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            window: Cửa sổ tính toán
            std: Số độ lệch chuẩn
        
        Returns:
            DataFrame với Bollinger Bands
        """
        df = data.copy()
        
        bb = ta.volatility.BollingerBands(df['Close'], window=window, window_dev=std)
        df['BB_Upper'] = bb.bollinger_hband()
        df['BB_Middle'] = bb.bollinger_mavg()
        df['BB_Lower'] = bb.bollinger_lband()
        df['BB_Width'] = bb.bollinger_wband()
        df['BB_Position'] = bb.bollinger_pband()
        
        return df
    
    def add_stochastic(self, data: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> pd.DataFrame:
        """
        Thêm Stochastic Oscillator
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            k_window: Cửa sổ %K
            d_window: Cửa sổ %D
        
        Returns:
            DataFrame với Stochastic
        """
        df = data.copy()
        
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], 
                                                window=k_window, smooth_window=d_window)
        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()
        
        return df
    
    def add_atr(self, data: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Thêm Average True Range (ATR)
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            window: Cửa sổ tính toán
        
        Returns:
            DataFrame với ATR
        """
        df = data.copy()
        df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=window)
        return df
    
    def add_volume_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Thêm các chỉ báo volume
        
        Args:
            data: DataFrame với dữ liệu OHLCV
        
        Returns:
            DataFrame với volume indicators
        """
        df = data.copy()
        
        # Volume SMA
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        
        # On Balance Volume (OBV)
        df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
        
        # Volume Rate of Change
        df['Volume_ROC'] = df['Volume'].pct_change(periods=10)
        
        return df
    
    def add_support_resistance(self, data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Tính toán support và resistance levels
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            window: Cửa sổ tìm kiếm
        
        Returns:
            DataFrame với support/resistance levels
        """
        df = data.copy()
        
        # Pivot Points
        df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['R1'] = 2 * df['Pivot'] - df['Low']
        df['S1'] = 2 * df['Pivot'] - df['High']
        df['R2'] = df['Pivot'] + (df['High'] - df['Low'])
        df['S2'] = df['Pivot'] - (df['High'] - df['Low'])
        
        return df
    
    def add_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Thêm tất cả các chỉ báo kỹ thuật
        
        Args:
            data: DataFrame với dữ liệu OHLCV
        
        Returns:
            DataFrame với tất cả indicators
        """
        df = data.copy()
        
        # Moving Averages
        df = self.add_moving_averages(df)
        
        # Momentum Indicators
        df = self.add_rsi(df)
        df = self.add_macd(df)
        df = self.add_stochastic(df)
        
        # Volatility Indicators
        df = self.add_bollinger_bands(df)
        df = self.add_atr(df)
        
        # Volume Indicators
        df = self.add_volume_indicators(df)
        
        # Support/Resistance
        df = self.add_support_resistance(df)
        
        return df
    
    def get_trading_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Tạo tín hiệu giao dịch dựa trên các chỉ báo
        
        Args:
            data: DataFrame với các indicators
        
        Returns:
            Dictionary với các tín hiệu
        """
        signals = {}
        
        if len(data) < 50:
            return {"error": "Không đủ dữ liệu để phân tích"}
        
        latest = data.iloc[-1]
        
        # RSI Signals
        if latest['RSI'] > 70:
            signals['RSI'] = 'SELL'
        elif latest['RSI'] < 30:
            signals['RSI'] = 'BUY'
        else:
            signals['RSI'] = 'NEUTRAL'
        
        # MACD Signals
        if latest['MACD'] > latest['MACD_Signal']:
            signals['MACD'] = 'BUY'
        else:
            signals['MACD'] = 'SELL'
        
        # Bollinger Bands Signals
        if latest['Close'] > latest['BB_Upper']:
            signals['BB'] = 'SELL'
        elif latest['Close'] < latest['BB_Lower']:
            signals['BB'] = 'BUY'
        else:
            signals['BB'] = 'NEUTRAL'
        
        # Moving Average Signals
        if latest['Close'] > latest['SMA_50'] > latest['SMA_200']:
            signals['MA'] = 'STRONG_BUY'
        elif latest['Close'] < latest['SMA_50'] < latest['SMA_200']:
            signals['MA'] = 'STRONG_SELL'
        elif latest['Close'] > latest['SMA_50']:
            signals['MA'] = 'BUY'
        else:
            signals['MA'] = 'SELL'
        
        # Overall Signal
        buy_signals = sum(1 for signal in signals.values() if 'BUY' in signal)
        sell_signals = sum(1 for signal in signals.values() if 'SELL' in signal)
        
        if buy_signals > sell_signals:
            signals['OVERALL'] = 'BUY'
        elif sell_signals > buy_signals:
            signals['OVERALL'] = 'SELL'
        else:
            signals['OVERALL'] = 'NEUTRAL'
        
        return signals
    
    def detect_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """
        Phát hiện các mô hình giá (candlestick patterns)
        
        Args:
            data: DataFrame với dữ liệu OHLCV
        
        Returns:
            List các patterns được phát hiện
        """
        patterns = []
        
        if len(data) < 5:
            return patterns
        
        # Doji Pattern
        for i in range(1, len(data)):
            current = data.iloc[i]
            prev = data.iloc[i-1]
            
            # Doji
            body_size = abs(current['Close'] - current['Open'])
            total_range = current['High'] - current['Low']
            
            if body_size / total_range < 0.1:  # Body nhỏ hơn 10% của range
                patterns.append({
                    'date': current.name,
                    'pattern': 'Doji',
                    'signal': 'Neutral',
                    'strength': 'Medium'
                })
            
            # Hammer
            if (current['Close'] > current['Open'] and  # Bullish candle
                (current['High'] - current['Close']) / (current['Close'] - current['Open']) < 0.3 and
                (current['Open'] - current['Low']) / (current['Close'] - current['Open']) > 2):
                patterns.append({
                    'date': current.name,
                    'pattern': 'Hammer',
                    'signal': 'Bullish',
                    'strength': 'Strong'
                })
        
        return patterns

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test technical analyzer
    from src.data.data_collector import DataCollector
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    
    # Lấy dữ liệu và phân tích
    data = collector.get_stock_data("AAPL", period="6mo")
    if not data.empty:
        # Thêm tất cả indicators
        data_with_indicators = analyzer.add_all_indicators(data)
        
        # Lấy tín hiệu giao dịch
        signals = analyzer.get_trading_signals(data_with_indicators)
        print("Trading Signals:", signals)
        
        # Phát hiện patterns
        patterns = analyzer.detect_patterns(data)
        print(f"Detected {len(patterns)} patterns")
        
        # Lưu kết quả
        data_with_indicators.to_csv("data/aapl_with_indicators.csv")
        print("Đã lưu dữ liệu với indicators") 