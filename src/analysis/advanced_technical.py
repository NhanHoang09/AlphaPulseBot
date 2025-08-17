"""
Advanced Technical Analysis Module
Phân tích kỹ thuật nâng cao với Fibonacci, Elliott Wave, Volume Profile
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta

class AdvancedTechnicalAnalyzer:
    """Class phân tích kỹ thuật nâng cao"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Fibonacci levels
        self.fibonacci_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        
        # Elliott Wave patterns
        self.elliott_patterns = {
            'impulse': [1, 2, 3, 4, 5],
            'correction': ['A', 'B', 'C'],
            'triangle': ['A', 'B', 'C', 'D', 'E']
        }
    
    def calculate_fibonacci_retracements(self, data: pd.DataFrame, 
                                       swing_high: float, swing_low: float) -> Dict:
        """
        Tính toán Fibonacci retracements
        
        Args:
            data: Dữ liệu giá
            swing_high: Đỉnh cao nhất
            swing_low: Đáy thấp nhất
        
        Returns:
            Dictionary với Fibonacci levels
        """
        try:
            price_range = swing_high - swing_low
            
            fib_levels = {}
            for level in self.fibonacci_levels:
                if level <= 1.0:  # Retracement levels
                    fib_price = swing_high - (price_range * level)
                    fib_levels[f'fib_{int(level*1000)}'] = fib_price
                else:  # Extension levels
                    fib_price = swing_high + (price_range * (level - 1))
                    fib_levels[f'fib_ext_{int(level*1000)}'] = fib_price
            
            return {
                'swing_high': swing_high,
                'swing_low': swing_low,
                'price_range': price_range,
                'levels': fib_levels,
                'current_price': data['Close'].iloc[-1] if not data.empty else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating Fibonacci retracements: {str(e)}")
            return {}
    
    def find_swing_points(self, data: pd.DataFrame, window: int = 20) -> Dict:
        """
        Tìm swing high và swing low
        
        Args:
            data: Dữ liệu giá
            window: Cửa sổ tìm kiếm
        
        Returns:
            Dictionary với swing points
        """
        try:
            if len(data) < window * 2:
                return {}
            
            highs = data['High'].rolling(window=window, center=True).max()
            lows = data['Low'].rolling(window=window, center=True).min()
            
            # Find swing highs
            swing_highs = []
            for i in range(window, len(data) - window):
                if data['High'].iloc[i] == highs.iloc[i]:
                    swing_highs.append({
                        'index': i,
                        'price': data['High'].iloc[i],
                        'date': data.index[i]
                    })
            
            # Find swing lows
            swing_lows = []
            for i in range(window, len(data) - window):
                if data['Low'].iloc[i] == lows.iloc[i]:
                    swing_lows.append({
                        'index': i,
                        'price': data['Low'].iloc[i],
                        'date': data.index[i]
                    })
            
            return {
                'swing_highs': swing_highs[-5:],  # Last 5 swing highs
                'swing_lows': swing_lows[-5:],    # Last 5 swing lows
                'current_swing_high': max([h['price'] for h in swing_highs[-3:]]) if swing_highs else 0,
                'current_swing_low': min([l['price'] for l in swing_lows[-3:]]) if swing_lows else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error finding swing points: {str(e)}")
            return {}
    
    def calculate_volume_profile(self, data: pd.DataFrame, bins: int = 50) -> Dict:
        """
        Tính toán Volume Profile
        
        Args:
            data: Dữ liệu giá với volume
            bins: Số bins cho histogram
        
        Returns:
            Dictionary với volume profile
        """
        try:
            if 'Volume' not in data.columns:
                return {'error': 'Volume data not available'}
            
            # Price range
            price_min = data['Low'].min()
            price_max = data['High'].max()
            price_range = price_max - price_min
            
            # Create price bins
            bin_size = price_range / bins
            price_bins = np.arange(price_min, price_max + bin_size, bin_size)
            
            # Calculate volume for each price level
            volume_profile = {}
            for i in range(len(price_bins) - 1):
                bin_low = price_bins[i]
                bin_high = price_bins[i + 1]
                
                # Find data points in this price range
                mask = (data['Low'] <= bin_high) & (data['High'] >= bin_low)
                volume_sum = data.loc[mask, 'Volume'].sum()
                
                price_level = (bin_low + bin_high) / 2
                volume_profile[price_level] = volume_sum
            
            # Find POC (Point of Control)
            poc_price = max(volume_profile, key=volume_profile.get)
            poc_volume = volume_profile[poc_price]
            
            # Find Value Area (70% of volume)
            total_volume = sum(volume_profile.values())
            target_volume = total_volume * 0.7
            
            sorted_levels = sorted(volume_profile.items(), key=lambda x: x[1], reverse=True)
            value_area_high = sorted_levels[0][0]
            value_area_low = sorted_levels[0][0]
            cumulative_volume = sorted_levels[0][1]
            
            for price, volume in sorted_levels[1:]:
                if cumulative_volume < target_volume:
                    value_area_high = max(value_area_high, price)
                    value_area_low = min(value_area_low, price)
                    cumulative_volume += volume
                else:
                    break
            
            return {
                'volume_profile': volume_profile,
                'poc_price': poc_price,
                'poc_volume': poc_volume,
                'value_area_high': value_area_high,
                'value_area_low': value_area_low,
                'total_volume': total_volume,
                'current_price': data['Close'].iloc[-1] if not data.empty else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating volume profile: {str(e)}")
            return {}
    
    def detect_elliott_wave_pattern(self, data: pd.DataFrame) -> Dict:
        """
        Phát hiện mô hình Elliott Wave (simplified)
        
        Args:
            data: Dữ liệu giá
        
        Returns:
            Dictionary với Elliott Wave pattern
        """
        try:
            # Simplified Elliott Wave detection
            # In real implementation, this would be much more complex
            
            if len(data) < 50:
                return {'error': 'Insufficient data for Elliott Wave analysis'}
            
            # Find potential wave structure
            swing_points = self.find_swing_points(data)
            
            if not swing_points:
                return {'error': 'No swing points found'}
            
            # Analyze recent price action
            recent_data = data.tail(20)
            price_change = (recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]
            
            # Simple pattern detection
            if price_change > 0.05:  # Strong uptrend
                pattern = 'Impulse Wave (Uptrend)'
                wave_count = 5
                current_wave = 'Wave 3 or 5'
            elif price_change < -0.05:  # Strong downtrend
                pattern = 'Impulse Wave (Downtrend)'
                wave_count = 5
                current_wave = 'Wave 3 or 5'
            else:
                pattern = 'Correction Wave'
                wave_count = 3
                current_wave = 'Wave A, B, or C'
            
            return {
                'pattern': pattern,
                'wave_count': wave_count,
                'current_wave': current_wave,
                'trend_direction': 'Bullish' if price_change > 0 else 'Bearish',
                'confidence': 0.6,  # Placeholder confidence
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting Elliott Wave pattern: {str(e)}")
            return {'error': f'Elliott Wave analysis error: {str(e)}'}
    
    def calculate_ichimoku_cloud(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Tính toán Ichimoku Cloud
        
        Args:
            data: Dữ liệu giá
        
        Returns:
            DataFrame với Ichimoku indicators
        """
        try:
            df = data.copy()
            
            # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
            period9_high = df['High'].rolling(window=9).max()
            period9_low = df['Low'].rolling(window=9).min()
            df['tenkan_sen'] = (period9_high + period9_low) / 2
            
            # Kijun-sen (Base Line): (26-period high + 26-period low)/2
            period26_high = df['High'].rolling(window=26).max()
            period26_low = df['Low'].rolling(window=26).min()
            df['kijun_sen'] = (period26_high + period26_low) / 2
            
            # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2
            df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
            
            # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
            period52_high = df['High'].rolling(window=52).max()
            period52_low = df['Low'].rolling(window=52).min()
            df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)
            
            # Chikou Span (Lagging Span): Close price shifted back 26 periods
            df['chikou_span'] = df['Close'].shift(-26)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error calculating Ichimoku Cloud: {str(e)}")
            return data
    
    def analyze_order_flow(self, data: pd.DataFrame) -> Dict:
        """
        Phân tích Order Flow (simplified)
        
        Args:
            data: Dữ liệu giá
        
        Returns:
            Dictionary với order flow analysis
        """
        try:
            if len(data) < 20:
                return {'error': 'Insufficient data for order flow analysis'}
            
            # Calculate basic order flow metrics
            recent_data = data.tail(20)
            
            # Volume analysis
            avg_volume = recent_data['Volume'].mean()
            current_volume = recent_data['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Price action analysis
            price_change = (recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]
            
            # Determine order flow sentiment
            if price_change > 0.02 and volume_ratio > 1.2:
                sentiment = 'Strong Buying Pressure'
                strength = 'High'
            elif price_change > 0.01 and volume_ratio > 1.0:
                sentiment = 'Moderate Buying Pressure'
                strength = 'Medium'
            elif price_change < -0.02 and volume_ratio > 1.2:
                sentiment = 'Strong Selling Pressure'
                strength = 'High'
            elif price_change < -0.01 and volume_ratio > 1.0:
                sentiment = 'Moderate Selling Pressure'
                strength = 'Medium'
            else:
                sentiment = 'Neutral Order Flow'
                strength = 'Low'
            
            return {
                'sentiment': sentiment,
                'strength': strength,
                'volume_ratio': volume_ratio,
                'price_change': price_change,
                'avg_volume': avg_volume,
                'current_volume': current_volume,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing order flow: {str(e)}")
            return {'error': f'Order flow analysis error: {str(e)}'}
    
    def generate_advanced_technical_report(self, data: pd.DataFrame, symbol: str) -> Dict:
        """
        Tạo báo cáo phân tích kỹ thuật nâng cao
        
        Args:
            data: Dữ liệu giá
            symbol: Mã cổ phiếu
        
        Returns:
            Dictionary với báo cáo phân tích nâng cao
        """
        try:
            report = {
                'symbol': symbol,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'current_price': data['Close'].iloc[-1] if not data.empty else 0
            }
            
            # Fibonacci Analysis
            swing_points = self.find_swing_points(data)
            if swing_points:
                fib_analysis = self.calculate_fibonacci_retracements(
                    data, 
                    swing_points['current_swing_high'],
                    swing_points['current_swing_low']
                )
                report['fibonacci'] = fib_analysis
            
            # Volume Profile
            volume_profile = self.calculate_volume_profile(data)
            if 'error' not in volume_profile:
                report['volume_profile'] = volume_profile
            
            # Elliott Wave
            elliott_wave = self.detect_elliott_wave_pattern(data)
            if 'error' not in elliott_wave:
                report['elliott_wave'] = elliott_wave
            
            # Ichimoku Cloud
            ichimoku_data = self.calculate_ichimoku_cloud(data)
            if not ichimoku_data.empty:
                latest = ichimoku_data.iloc[-1]
                report['ichimoku'] = {
                    'tenkan_sen': latest.get('tenkan_sen', 0),
                    'kijun_sen': latest.get('kijun_sen', 0),
                    'senkou_span_a': latest.get('senkou_span_a', 0),
                    'senkou_span_b': latest.get('senkou_span_b', 0),
                    'chikou_span': latest.get('chikou_span', 0)
                }
            
            # Order Flow
            order_flow = self.analyze_order_flow(data)
            if 'error' not in order_flow:
                report['order_flow'] = order_flow
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating advanced technical report: {str(e)}")
            return {'error': f'Advanced technical analysis error: {str(e)}'}
