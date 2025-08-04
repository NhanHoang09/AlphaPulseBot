"""
Vietnam Stock Market Data Collector
Thu thập dữ liệu thị trường chứng khoán Việt Nam
"""

import pandas as pd
import numpy as np
import requests
import yfinance as yf
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import time

class VNDataCollector:
    """Class thu thập dữ liệu thị trường chứng khoán Việt Nam"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://finfo-api.vndirect.com.vn/v4"
        
    def get_vn_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Lấy dữ liệu cổ phiếu VN từ VNDIRECT API
        
        Args:
            symbol: Mã cổ phiếu (e.g., 'VNM', 'TCB', 'HPG')
            period: Khoảng thời gian ('1d', '1w', '1m', '3m', '6m', '1y', '2y', '5y')
        
        Returns:
            DataFrame với dữ liệu OHLCV
        """
        try:
            # Tính toán ngày bắt đầu và kết thúc
            end_date = datetime.now()
            if period == "1d":
                start_date = end_date - timedelta(days=1)
            elif period == "1w":
                start_date = end_date - timedelta(weeks=1)
            elif period == "1m":
                start_date = end_date - timedelta(days=30)
            elif period == "3m":
                start_date = end_date - timedelta(days=90)
            elif period == "6m":
                start_date = end_date - timedelta(days=180)
            elif period == "1y":
                start_date = end_date - timedelta(days=365)
            elif period == "2y":
                start_date = end_date - timedelta(days=730)
            elif period == "5y":
                start_date = end_date - timedelta(days=1825)
            else:
                start_date = end_date - timedelta(days=365)
            
            # Format dates
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # API endpoint
            url = f"{self.base_url}/stock_prices"
            params = {
                'sort': 'date',
                'q': f'code:{symbol}',
                'size': 1000,
                'from': start_str,
                'to': end_str
            }
            
            self.logger.info(f"Đang lấy dữ liệu cho {symbol} từ {start_str} đến {end_str}")
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('data'):
                self.logger.warning(f"Không có dữ liệu cho {symbol}")
                return pd.DataFrame()
            
            # Chuyển đổi dữ liệu
            df = pd.DataFrame(data['data'])
            
            # Đổi tên cột
            column_mapping = {
                'date': 'Date',
                'code': 'Symbol',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume',
                'value': 'Value'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Chuyển đổi kiểu dữ liệu
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            # Chuyển đổi giá từ VND sang số thực
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = df[col].astype(float) / 1000  # Chia cho 1000 vì giá VN thường nhân 1000
            
            # Tính toán thêm các cột
            df['Returns'] = df['Close'].pct_change()
            df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
            df['Volatility'] = df['Returns'].rolling(window=20).std()
            
            self.logger.info(f"Đã lấy {len(df)} điểm dữ liệu cho {symbol}")
            return df
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu cho {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_vn_index_data(self, index_code: str = "VNINDEX", period: str = "1y") -> pd.DataFrame:
        """
        Lấy dữ liệu chỉ số VN
        
        Args:
            index_code: Mã chỉ số ('VNINDEX', 'HNXINDEX', 'VN30', 'HNX30')
            period: Khoảng thời gian
        
        Returns:
            DataFrame với dữ liệu chỉ số
        """
        try:
            # Tính toán ngày
            end_date = datetime.now()
            if period == "1y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=365)
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # API endpoint cho chỉ số
            url = f"{self.base_url}/indices"
            params = {
                'sort': 'date',
                'q': f'code:{index_code}',
                'size': 1000,
                'from': start_str,
                'to': end_str
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('data'):
                self.logger.warning(f"Không có dữ liệu cho chỉ số {index_code}")
                return pd.DataFrame()
            
            df = pd.DataFrame(data['data'])
            
            # Đổi tên cột
            column_mapping = {
                'date': 'Date',
                'code': 'Symbol',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume',
                'value': 'Value'
            }
            
            df = df.rename(columns=column_mapping)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            # Tính toán thêm
            df['Returns'] = df['Close'].pct_change()
            df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
            df['Volatility'] = df['Returns'].rolling(window=20).std()
            
            return df
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu chỉ số {index_code}: {str(e)}")
            return pd.DataFrame()
    
    def get_vn_stock_list(self) -> List[Dict]:
        """
        Lấy danh sách cổ phiếu VN
        
        Returns:
            List các cổ phiếu với thông tin cơ bản
        """
        try:
            url = f"{self.base_url}/companies"
            params = {
                'sort': 'marketCap',
                'size': 1000
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('data', [])
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy danh sách cổ phiếu: {str(e)}")
            return []
    
    def get_vn_market_summary(self) -> Dict:
        """
        Lấy tổng quan thị trường VN
        
        Returns:
            Dictionary với thông tin tổng quan
        """
        try:
            # Lấy VNINDEX
            vnindex = self.get_vn_index_data("VNINDEX", "1d")
            
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
            data = self.get_vn_stock_data(symbol, period)
            if not data.empty:
                data_dict[symbol] = data
            time.sleep(0.5)  # Tránh rate limiting
        
        return data_dict

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test VN data collector
    vn_collector = VNDataCollector()
    
    # Test lấy dữ liệu VNM
    print("🔍 Lấy dữ liệu VNM...")
    vnm_data = vn_collector.get_vn_stock_data("VNM", period="6mo")
    if not vnm_data.empty:
        print(f"✅ Đã lấy {len(vnm_data)} điểm dữ liệu cho VNM")
        print(f"   Giá hiện tại: {vnm_data['Close'].iloc[-1]:,.0f} VND")
        print(f"   Thay đổi: {vnm_data['Returns'].iloc[-1]*100:.2f}%")
    
    # Test lấy VNINDEX
    print("\n🔍 Lấy dữ liệu VNINDEX...")
    vnindex_data = vn_collector.get_vn_index_data("VNINDEX", period="1mo")
    if not vnindex_data.empty:
        print(f"✅ Đã lấy {len(vnindex_data)} điểm dữ liệu cho VNINDEX")
        print(f"   Giá hiện tại: {vnindex_data['Close'].iloc[-1]:,.2f}")
    
    # Test tổng quan thị trường
    print("\n🔍 Tổng quan thị trường...")
    summary = vn_collector.get_vn_market_summary()
    if summary:
        print(f"✅ {summary['index']}: {summary['current_value']:,.2f}")
        print(f"   Thay đổi: {summary['change']:+.2f} ({summary['change_pct']:+.2f}%)") 