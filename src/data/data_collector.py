"""
Data Collector Module
Thu thập dữ liệu thị trường từ các nguồn khác nhau
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataCollector:
    """Class thu thập dữ liệu thị trường"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
    def get_stock_data(self, symbol: str, period: str = "1y", interval: str = "1d", market: str = "US") -> pd.DataFrame:
        """
        Lấy dữ liệu cổ phiếu từ Yahoo Finance hoặc VNDIRECT
        
        Args:
            symbol: Mã cổ phiếu (e.g., 'AAPL', 'MSFT', 'VNM', 'TCB')
            period: Khoảng thời gian ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Khoảng thời gian giữa các điểm dữ liệu ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
            market: Thị trường ('US' hoặc 'VN')
        
        Returns:
            DataFrame với dữ liệu OHLCV
        """
        try:
            if market.upper() == "VN":
                # Sử dụng VNDIRECT API cho thị trường VN
                from .vn_data_collector import VNDataCollector
                vn_collector = VNDataCollector()
                return vn_collector.get_vn_stock_data(symbol, period)
            else:
                # Sử dụng Yahoo Finance cho thị trường US
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period, interval=interval)
                
                if data.empty:
                    self.logger.warning(f"Không có dữ liệu cho {symbol}")
                    return pd.DataFrame()
                
                # Thêm các cột tính toán
                data['Returns'] = data['Close'].pct_change()
                data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
                data['Volatility'] = data['Returns'].rolling(window=20).std()
                
                self.logger.info(f"Đã lấy dữ liệu cho {symbol}: {len(data)} điểm dữ liệu")
                return data
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu cho {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_crypto_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Lấy dữ liệu cryptocurrency
        
        Args:
            symbol: Mã crypto (e.g., 'BTC-USD', 'ETH-USD')
            period: Khoảng thời gian
            interval: Khoảng thời gian giữa các điểm dữ liệu
        
        Returns:
            DataFrame với dữ liệu OHLCV
        """
        return self.get_stock_data(symbol, period, interval)
    
    def get_forex_data(self, from_currency: str, to_currency: str, 
                      period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Lấy dữ liệu forex
        
        Args:
            from_currency: Tiền tệ gốc (e.g., 'USD')
            to_currency: Tiền tệ đích (e.g., 'EUR')
            period: Khoảng thời gian
            interval: Khoảng thời gian giữa các điểm dữ liệu
        
        Returns:
            DataFrame với dữ liệu OHLCV
        """
        symbol = f"{from_currency}{to_currency}=X"
        return self.get_stock_data(symbol, period, interval)
    
    def get_market_data_batch(self, symbols: List[str], period: str = "1y", 
                             interval: str = "1d") -> Dict[str, pd.DataFrame]:
        """
        Lấy dữ liệu cho nhiều symbols cùng lúc
        
        Args:
            symbols: Danh sách các symbols
            period: Khoảng thời gian
            interval: Khoảng thời gian giữa các điểm dữ liệu
        
        Returns:
            Dictionary với key là symbol và value là DataFrame
        """
        data_dict = {}
        
        for symbol in symbols:
            data = self.get_stock_data(symbol, period, interval)
            if not data.empty:
                data_dict[symbol] = data
            time.sleep(0.1)  # Tránh rate limiting
        
        return data_dict
    
    def get_news_sentiment(self, symbol: str, days: int = 7) -> pd.DataFrame:
        """
        Lấy dữ liệu sentiment từ news (cần News API key)
        
        Args:
            symbol: Mã cổ phiếu
            days: Số ngày lấy dữ liệu
        
        Returns:
            DataFrame với sentiment data
        """
        # Placeholder - cần implement với News API
        self.logger.info(f"News sentiment cho {symbol} - chưa implement")
        return pd.DataFrame()
    
    def get_economic_indicators(self) -> pd.DataFrame:
        """
        Lấy các chỉ số kinh tế vĩ mô
        
        Returns:
            DataFrame với economic indicators
        """
        # Placeholder - có thể sử dụng FRED API
        self.logger.info("Economic indicators - chưa implement")
        return pd.DataFrame()
    
    def save_data(self, data: pd.DataFrame, symbol: str, data_type: str = "stock") -> str:
        """
        Lưu dữ liệu vào file
        
        Args:
            data: DataFrame cần lưu
            symbol: Mã symbol
            data_type: Loại dữ liệu ('stock', 'crypto', 'forex')
        
        Returns:
            Đường dẫn file đã lưu
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/{data_type}_{symbol}_{timestamp}.csv"
        
        # Tạo thư mục nếu chưa có
        os.makedirs("data", exist_ok=True)
        
        data.to_csv(filename)
        self.logger.info(f"Đã lưu dữ liệu vào {filename}")
        return filename
    
    def load_data(self, filename: str) -> pd.DataFrame:
        """
        Load dữ liệu từ file
        
        Args:
            filename: Tên file cần load
        
        Returns:
            DataFrame với dữ liệu
        """
        try:
            data = pd.read_csv(filename, index_col=0, parse_dates=True)
            self.logger.info(f"Đã load dữ liệu từ {filename}")
            return data
        except Exception as e:
            self.logger.error(f"Lỗi khi load dữ liệu từ {filename}: {str(e)}")
            return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test data collector
    collector = DataCollector()
    
    # Lấy dữ liệu Apple
    apple_data = collector.get_stock_data("AAPL", period="6mo")
    print(f"Apple data shape: {apple_data.shape}")
    print(apple_data.head())
    
    # Lấy dữ liệu Bitcoin
    btc_data = collector.get_crypto_data("BTC-USD", period="1mo")
    print(f"Bitcoin data shape: {btc_data.shape}")
    print(btc_data.head()) 