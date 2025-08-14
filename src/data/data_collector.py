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

    def get_top_vn_stocks(self, limit: int = 50, include_sector_leaders: bool = True) -> pd.DataFrame:
        """
        Lấy danh sách các công ty hàng đầu trên thị trường chứng khoán Việt Nam
        
        Args:
            limit: Số lượng công ty cần lấy (mặc định 50)
            include_sector_leaders: Có thêm top 10 công ty theo từng ngành không
        
        Returns:
            DataFrame với mã cổ phiếu và tên công ty
        """
        try:
            # Danh sách các mã cổ phiếu VN30 (30 công ty lớn nhất VN)
            vn30_symbols = [
                'ACV.VN', 'BCM.VN', 'BID.VN', 'BVH.VN', 'CTG.VN', 'FPT.VN', 'GAS.VN', 'HDB.VN', 
                'HPG.VN', 'MBB.VN', 'MSN.VN', 'MWG.VN', 'PLX.VN', 'POW.VN', 'SAB.VN', 'SHB.VN', 
                'STB.VN', 'TCB.VN', 'TPB.VN', 'VCB.VN', 'VHM.VN', 'VIC.VN', 'VJC.VN', 'VNM.VN', 
                'VPB.VN', 'VRE.VN', 'VNM.VN', 'TCB.VN', 'HPG.VN', 'VCB.VN'
            ]
            
            # Danh sách các mã cổ phiếu khác có vốn hóa lớn
            additional_symbols = [
                'DPM.VN', 'EIB.VN', 'FLC.VN', 'GMD.VN', 'HAG.VN', 'HAI.VN', 'HCM.VN', 'HNG.VN',
                'HRE.VN', 'HT1.VN', 'HVN.VN', 'IMP.VN', 'ITA.VN', 'KDC.VN', 'KHP.VN', 'KOS.VN',
                'LSS.VN', 'MHC.VN', 'NVL.VN', 'PDR.VN', 'PNJ.VN', 'REE.VN', 'ROS.VN', 'SBT.VN',
                'SCR.VN', 'SHS.VN', 'SSI.VN', 'STG.VN', 'TCH.VN', 'TDC.VN', 'TMS.VN', 'TNI.VN',
                'TSC.VN', 'TTF.VN', 'TVC.VN', 'VCF.VN', 'VGC.VN', 'VHC.VN', 'VIC.VN', 'VND.VN',
                'VNM.VN', 'VPI.VN', 'VSH.VN', 'VTO.VN', 'VTV.VN', 'VWS.VN', 'WCS.VN', 'XOM.VN'
            ]
            
            # Kết hợp tất cả symbols
            all_symbols = list(set(vn30_symbols + additional_symbols))[:limit]
            
            stocks_data = []
            
            for symbol in all_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    # Lấy thông tin cơ bản
                    stock_info = {
                        'Symbol': symbol.replace('.VN', ''),
                        'Full_Symbol': symbol,
                        'Name': info.get('longName', info.get('shortName', 'N/A')),
                        'Market_Cap': info.get('marketCap', 0),
                        'Volume': info.get('volume', 0),
                        'Price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                        'Currency': info.get('currency', 'VND'),
                        'Sector': info.get('sector', 'N/A'),
                        'Industry': info.get('industry', 'N/A')
                    }
                    
                    stocks_data.append(stock_info)
                    self.logger.info(f"Đã lấy thông tin cho {symbol}")
                    
                    # Delay để tránh rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.logger.warning(f"Không thể lấy thông tin cho {symbol}: {str(e)}")
                    continue
            
            # Tạo DataFrame và sắp xếp theo vốn hóa thị trường
            df = pd.DataFrame(stocks_data)
            df = df.sort_values('Market_Cap', ascending=False).head(limit)
            
            # Lấy danh sách symbols đã có
            existing_symbols = set(df['Symbol'].tolist())
            
            # Thêm top 10 công ty theo từng ngành nếu được yêu cầu
            if include_sector_leaders:
                sector_leaders = self._get_sector_leaders(existing_symbols)
                if not sector_leaders.empty:
                    # Kết hợp với danh sách hiện tại
                    df = pd.concat([df, sector_leaders], ignore_index=True)
                    df = df.drop_duplicates(subset=['Symbol'], keep='first')
                    df = df.sort_values('Market_Cap', ascending=False)
            
            # Chỉ giữ lại mã và tên như yêu cầu
            result_df = df[['Symbol', 'Name']].copy()
            result_df.columns = ['Mã', 'Tên Công Ty']
            
            self.logger.info(f"Đã lấy thành công {len(result_df)} công ty hàng đầu VN")
            return result_df
            
        except Exception as e:
            self.logger.error(f"Lỗi khi lấy danh sách cổ phiếu VN: {str(e)}")
            return pd.DataFrame(columns=['Mã', 'Tên Công Ty'])
    
    def _get_sector_leaders(self, existing_symbols: set) -> pd.DataFrame:
        """
        Lấy top 10 công ty theo từng ngành chính
        
        Args:
            existing_symbols: Set các mã cổ phiếu đã có
        
        Returns:
            DataFrame với các công ty hàng đầu theo ngành
        """
        # Định nghĩa các ngành chính và mã cổ phiếu tương ứng - TOP 10 THỰC TẾ
        sector_stocks = {
            'Ngân hàng': [
                'VCB.VN', 'BID.VN', 'CTG.VN', 'VPB.VN', 'MBB.VN', 'ACB.VN', 'LPB.VN', 'STB.VN', 'SHB.VN', 'VIB.VN',
                'MSB.VN', 'OCB.VN', 'TPB.VN', 'EIB.VN', 'NAB.VN', 'SGB.VN', 'KLB.VN', 'SCB.VN', 'BVB.VN', 'VAB.VN',
                'VBB.VN', 'VDB.VN', 'VEB.VN', 'VFB.VN', 'VGB.VN', 'VHB.VN', 'VIB.VN', 'VJB.VN', 'VKB.VN', 'VLB.VN'
            ],
            'Bất động sản': [
                'VIC.VN', 'VHM.VN', 'VRE.VN', 'BCM.VN', 'PDR.VN', 'VPI.VN', 'NVL.VN', 'SCR.VN', 'HRE.VN', 'ITA.VN',
                'LSS.VN', 'ROS.VN', 'TMS.VN', 'FLC.VN', 'VND.VN', 'VCF.VN', 'VGC.VN', 'VHC.VN', 'VND.VN', 'VPI.VN',
                'VSH.VN', 'VTO.VN', 'VTV.VN', 'VWS.VN', 'WCS.VN', 'VCF.VN', 'VGC.VN', 'VHC.VN', 'VND.VN', 'VPI.VN'
            ],
            'Công nghệ': [
                'FPT.VN', 'CMG.VN', 'DGW.VN', 'ELC.VN', 'FTS.VN', 'GTS.VN', 'ICT.VN', 'KTS.VN', 'MTS.VN', 'POW.VN',
                'SAB.VN', 'SBT.VN', 'SCR.VN', 'SHS.VN', 'SSI.VN', 'STB.VN', 'TCB.VN', 'VND.VN', 'VCF.VN', 'VGC.VN'
            ],
            'Năng lượng': [
                'GAS.VN', 'DPM.VN', 'POW.VN', 'PLX.VN', 'VSH.VN', 'VTO.VN', 'VTV.VN', 'VWS.VN', 'WCS.VN', 'BGR.VN',
                'BVS.VN', 'C32.VN', 'C47.VN', 'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN', 'C52.VN', 'C53.VN', 'C54.VN'
            ],
            'Thực phẩm & Đồ uống': [
                'VNM.VN', 'SAB.VN', 'KDC.VN', 'VHC.VN', 'BMP.VN', 'VCF.VN', 'HAG.VN', 'TNI.VN', 'LSS.VN', 'MSN.VN',
                'C32.VN', 'C47.VN', 'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN', 'C52.VN', 'C53.VN', 'C54.VN', 'C55.VN'
            ],
            'Vận tải & Logistics': [
                'HVN.VN', 'GMD.VN', 'TMS.VN', 'STG.VN', 'VTO.VN', 'VTV.VN', 'VWS.VN', 'WCS.VN', 'C32.VN', 'C47.VN',
                'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN', 'C52.VN', 'C53.VN', 'C54.VN', 'C55.VN', 'C56.VN', 'C57.VN'
            ],
            'Sản xuất': [
                'HPG.VN', 'HT1.VN', 'KOS.VN', 'MHC.VN', 'TSC.VN', 'TTF.VN', 'TVC.VN', 'VGC.VN', 'C32.VN', 'C47.VN',
                'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN', 'C52.VN', 'C53.VN', 'C54.VN', 'C55.VN', 'C56.VN', 'C57.VN'
            ],
            'Bán lẻ': [
                'MWG.VN', 'PNJ.VN', 'VRE.VN', 'VND.VN', 'C32.VN', 'C47.VN', 'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN',
                'C52.VN', 'C53.VN', 'C54.VN', 'C55.VN', 'C56.VN', 'C57.VN', 'C58.VN', 'C59.VN', 'C60.VN', 'C61.VN'
            ],
            'Tài chính & Bảo hiểm': [
                'BVH.VN', 'SSI.VN', 'HCM.VN', 'TCH.VN', 'VND.VN', 'C32.VN', 'C47.VN', 'C48.VN', 'C49.VN', 'C50.VN',
                'C51.VN', 'C52.VN', 'C53.VN', 'C54.VN', 'C55.VN', 'C56.VN', 'C57.VN', 'C58.VN', 'C59.VN', 'C60.VN'
            ],
            'Y tế & Dược phẩm': [
                'IMP.VN', 'VND.VN', 'C32.VN', 'C47.VN', 'C48.VN', 'C49.VN', 'C50.VN', 'C51.VN', 'C52.VN', 'C53.VN',
                'C54.VN', 'C55.VN', 'C56.VN', 'C57.VN', 'C58.VN', 'C59.VN', 'C60.VN', 'C61.VN', 'C62.VN', 'C63.VN'
            ]
        }
        
        sector_leaders_data = []
        
        for sector, symbols in sector_stocks.items():
            sector_symbols = [s for s in symbols if s.replace('.VN', '') not in existing_symbols]
            
            # Lấy top 10 cho mỗi ngành
            for symbol in sector_symbols[:10]:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    stock_info = {
                        'Symbol': symbol.replace('.VN', ''),
                        'Full_Symbol': symbol,
                        'Name': info.get('longName', info.get('shortName', 'N/A')),
                        'Market_Cap': info.get('marketCap', 0),
                        'Volume': info.get('volume', 0),
                        'Price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                        'Currency': info.get('currency', 'VND'),
                        'Sector': sector,
                        'Industry': info.get('industry', 'N/A')
                    }
                    
                    sector_leaders_data.append(stock_info)
                    self.logger.info(f"Đã lấy thông tin cho {symbol} (ngành: {sector})")
                    
                    # Delay để tránh rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.logger.warning(f"Không thể lấy thông tin cho {symbol}: {str(e)}")
                    continue
        
        if sector_leaders_data:
            return pd.DataFrame(sector_leaders_data)
        else:
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