"""
Vietnam Stock Market Alternative Data Collector
Thu thập dữ liệu thị trường chứng khoán Việt Nam từ các nguồn khác
"""

import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import time

class VNAlternativeCollector:
    """Class thu thập dữ liệu thị trường chứng khoán Việt Nam từ các nguồn thay thế"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_vn_stock_data_yahoo(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Lấy dữ liệu cổ phiếu VN từ Yahoo Finance
        
        Args:
            symbol: Mã cổ phiếu (e.g., 'VNM.VN', 'TCB.VN')
            period: Khoảng thời gian
        
        Returns:
            DataFrame với dữ liệu OHLCV
        """
        try:
            # Thêm .VN suffix cho Yahoo Finance
            if not symbol.endswith('.VN'):
                yahoo_symbol = f"{symbol}.VN"
            else:
                yahoo_symbol = symbol
            
            self.logger.info(f"Đang lấy dữ liệu cho {yahoo_symbol} từ Yahoo Finance...")
            self.logger.info(f"Original symbol: {symbol}, Yahoo symbol: {yahoo_symbol}")
            
            ticker = yf.Ticker(yahoo_symbol)
            data = ticker.history(period=period)
            
            self.logger.info(f"Raw data from Yahoo: {data.shape if not data.empty else 'Empty'}")
            
            if data.empty:
                self.logger.warning(f"Không có dữ liệu cho {yahoo_symbol}")
                return pd.DataFrame()
            
            # Tính toán thêm các cột
            data['Returns'] = data['Close'].pct_change()
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Volatility'] = data['Returns'].rolling(window=20).std()
            
            self.logger.info(f"Đã lấy {len(data)} điểm dữ liệu cho {symbol}")
            self.logger.info(f"Final data columns: {data.columns.tolist()}")
            return data
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu cho {symbol}: {str(e)}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return pd.DataFrame()
    
    def get_vn_index_data_yahoo(self, index_code: str = "VNINDEX", period: str = "1y") -> pd.DataFrame:
        """
        Lấy dữ liệu chỉ số VN từ Yahoo Finance
        
        Args:
            index_code: Mã chỉ số ('VNINDEX', 'HNXINDEX')
            period: Khoảng thời gian
        
        Returns:
            DataFrame với dữ liệu chỉ số
        """
        try:
            # Map chỉ số VN cho Yahoo Finance
            index_mapping = {
                'VNINDEX': '^VNINDEX',
                'HNXINDEX': '^HNXINDEX'
            }
            
            yahoo_symbol = index_mapping.get(index_code, f"^{index_code}")
            
            self.logger.info(f"Đang lấy dữ liệu cho {yahoo_symbol} từ Yahoo Finance...")
            
            ticker = yf.Ticker(yahoo_symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                self.logger.warning(f"Không có dữ liệu cho {yahoo_symbol}")
                return pd.DataFrame()
            
            # Tính toán thêm
            data['Returns'] = data['Close'].pct_change()
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Volatility'] = data['Returns'].rolling(window=20).std()
            
            return data
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu chỉ số {index_code}: {str(e)}")
            return pd.DataFrame()
    
    def get_vn_stock_data_batch(self, symbols: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Lấy dữ liệu cho nhiều cổ phiếu VN cùng lúc
        
        Args:
            symbols: Danh sách mã cổ phiếu
            period: Khoảng thời gian
        
        Returns:
            Dictionary với key là symbol và value là DataFrame
        """
        data_dict = {}
        
        for symbol in symbols:
            data = self.get_vn_stock_data_yahoo(symbol, period)
            if not data.empty:
                data_dict[symbol] = data
            time.sleep(0.5)  # Tránh rate limiting
        
        return data_dict
    
    def get_vn_market_summary(self) -> Dict:
        """
        Lấy tổng quan thị trường VN
        
        Returns:
            Dictionary với thông tin tổng quan
        """
        try:
            # Lấy VNINDEX
            vnindex = self.get_vn_index_data_yahoo("VNINDEX", "1d")
            
            if vnindex.empty:
                return {}
            
            latest = vnindex.iloc[-1]
            prev = vnindex.iloc[-2] if len(vnindex) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_pct = (change / prev['Close']) * 100
            
            return {
                'index': 'VNINDEX',
                'current_value': latest['Close'],
                'change': change,
                'change_pct': change_pct,
                'volume': latest['Volume'],
                'date': latest.name.strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy tổng quan thị trường: {str(e)}")
            return {}
    
    def get_sample_vn_data(self) -> Dict[str, pd.DataFrame]:
        """
        Tạo dữ liệu mẫu cho demo (khi không thể kết nối API)
        
        Returns:
            Dictionary với dữ liệu mẫu
        """
        # Tạo dữ liệu mẫu cho VNM
        dates = pd.date_range(start='2024-01-01', end='2025-08-01', freq='D')
        np.random.seed(42)
        
        # VNM data
        vnm_prices = []
        base_price = 75000  # Giá cơ bản VNM
        
        for i in range(len(dates)):
            if i == 0:
                price = base_price
            else:
                # Tạo biến động giá thực tế
                daily_return = np.random.normal(0.001, 0.02)  # 0.1% trung bình, 2% độ lệch
                price = vnm_prices[-1] * (1 + daily_return)
            
            vnm_prices.append(price)
        
        vnm_data = pd.DataFrame({
            'Open': [p * (1 + np.random.normal(0, 0.005)) for p in vnm_prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in vnm_prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in vnm_prices],
            'Close': vnm_prices,
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)
        
        # Tính toán thêm
        vnm_data['Returns'] = vnm_data['Close'].pct_change()
        vnm_data['Log_Returns'] = np.log(vnm_data['Close'] / vnm_data['Close'].shift(1))
        vnm_data['Volatility'] = vnm_data['Returns'].rolling(window=20).std()
        
        # TCB data
        tcb_prices = []
        base_price_tcb = 25000  # Giá cơ bản TCB
        
        for i in range(len(dates)):
            if i == 0:
                price = base_price_tcb
            else:
                daily_return = np.random.normal(0.0015, 0.025)  # TCB biến động hơn
                price = tcb_prices[-1] * (1 + daily_return)
            
            tcb_prices.append(price)
        
        tcb_data = pd.DataFrame({
            'Open': [p * (1 + np.random.normal(0, 0.005)) for p in tcb_prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in tcb_prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in tcb_prices],
            'Close': tcb_prices,
            'Volume': np.random.randint(2000000, 8000000, len(dates))
        }, index=dates)
        
        # Tính toán thêm
        tcb_data['Returns'] = tcb_data['Close'].pct_change()
        tcb_data['Log_Returns'] = np.log(tcb_data['Close'] / tcb_data['Close'].shift(1))
        tcb_data['Volatility'] = tcb_data['Returns'].rolling(window=20).std()
        
        # VNINDEX data
        vnindex_prices = []
        base_price_index = 1200  # Giá cơ bản VNINDEX
        
        for i in range(len(dates)):
            if i == 0:
                price = base_price_index
            else:
                daily_return = np.random.normal(0.0008, 0.015)  # Index ít biến động hơn
                price = vnindex_prices[-1] * (1 + daily_return)
            
            vnindex_prices.append(price)
        
        vnindex_data = pd.DataFrame({
            'Open': [p * (1 + np.random.normal(0, 0.003)) for p in vnindex_prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.008))) for p in vnindex_prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.008))) for p in vnindex_prices],
            'Close': vnindex_prices,
            'Volume': np.random.randint(50000000, 200000000, len(dates))
        }, index=dates)
        
        # Tính toán thêm
        vnindex_data['Returns'] = vnindex_data['Close'].pct_change()
        vnindex_data['Log_Returns'] = np.log(vnindex_data['Close'] / vnindex_data['Close'].shift(1))
        vnindex_data['Volatility'] = vnindex_data['Returns'].rolling(window=20).std()
        
        return {
            'VNM': vnm_data,
            'TCB': tcb_data,
            'VNINDEX': vnindex_data
        }

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test VN alternative collector
    vn_collector = VNAlternativeCollector()
    
    # Test lấy dữ liệu VNM từ Yahoo Finance
    print("🔍 Lấy dữ liệu VNM từ Yahoo Finance...")
    vnm_data = vn_collector.get_vn_stock_data_yahoo("VNM", period="6mo")
    if not vnm_data.empty:
        print(f"✅ Đã lấy {len(vnm_data)} điểm dữ liệu cho VNM")
        print(f"   Giá hiện tại: {vnm_data['Close'].iloc[-1]:,.0f} VND")
        print(f"   Thay đổi: {vnm_data['Returns'].iloc[-1]*100:.2f}%")
    else:
        print("❌ Không thể lấy dữ liệu VNM từ Yahoo Finance")
        print("🔧 Sử dụng dữ liệu mẫu...")
        sample_data = vn_collector.get_sample_vn_data()
        vnm_data = sample_data['VNM']
        print(f"✅ Đã tạo {len(vnm_data)} điểm dữ liệu mẫu cho VNM")
        print(f"   Giá hiện tại: {vnm_data['Close'].iloc[-1]:,.0f} VND") 