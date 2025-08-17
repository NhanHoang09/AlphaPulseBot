"""
Fundamental Analysis Module
Phân tích cơ bản với các chỉ số tài chính quan trọng
"""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta

class FundamentalAnalyzer:
    """Class phân tích cơ bản"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Định nghĩa các ngưỡng đánh giá
        self.thresholds = {
            'pe_good': 15,
            'pe_high': 25,
            'pb_good': 1.5,
            'pb_high': 3.0,
            'roe_good': 0.15,
            'roe_excellent': 0.25,
            'debt_ratio_good': 0.5,
            'debt_ratio_high': 0.7,
            'current_ratio_good': 1.5,
            'current_ratio_excellent': 2.0,
            'profit_margin_good': 0.10,
            'profit_margin_excellent': 0.20
        }
    
    def get_fundamental_data(self, symbol: str, market: str = "US") -> Dict:
        """
        Lấy dữ liệu cơ bản cho một cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            market: Thị trường (US/VN)
        
        Returns:
            Dictionary với dữ liệu cơ bản
        """
        try:
            if market == "VN":
                # Thêm .VN suffix cho cổ phiếu VN
                ticker = yf.Ticker(f"{symbol}.VN")
            else:
                ticker = yf.Ticker(symbol)
            
            # Lấy thông tin cơ bản
            info = ticker.info
            
            # Lấy báo cáo tài chính
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            return {
                'info': info,
                'financials': financials,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow,
                'ticker': ticker
            }
            
        except Exception as e:
            self.logger.error(f"Error getting fundamental data for {symbol}: {str(e)}")
            return {}
    
    def calculate_valuation_ratios(self, fundamental_data: Dict) -> Dict:
        """
        Tính toán các chỉ số định giá
        
        Args:
            fundamental_data: Dữ liệu cơ bản
        
        Returns:
            Dictionary với các chỉ số định giá
        """
        try:
            info = fundamental_data.get('info', {})
            
            ratios = {}
            
            # P/E Ratio
            ratios['pe_ratio'] = info.get('trailingPE', None)
            ratios['forward_pe'] = info.get('forwardPE', None)
            
            # P/B Ratio
            ratios['pb_ratio'] = info.get('priceToBook', None)
            
            # P/S Ratio
            ratios['ps_ratio'] = info.get('priceToSalesTrailing12Months', None)
            
            # EV/EBITDA
            ratios['ev_ebitda'] = info.get('enterpriseToEbitda', None)
            
            # Dividend Yield
            ratios['dividend_yield'] = info.get('dividendYield', None)
            if ratios['dividend_yield']:
                ratios['dividend_yield'] *= 100  # Convert to percentage
            
            # Market Cap
            ratios['market_cap'] = info.get('marketCap', None)
            
            return ratios
            
        except Exception as e:
            self.logger.error(f"Error calculating valuation ratios: {str(e)}")
            return {}
    
    def calculate_profitability_ratios(self, fundamental_data: Dict) -> Dict:
        """
        Tính toán các chỉ số sinh lời
        
        Args:
            fundamental_data: Dữ liệu cơ bản
        
        Returns:
            Dictionary với các chỉ số sinh lời
        """
        try:
            info = fundamental_data.get('info', {})
            financials = fundamental_data.get('financials', pd.DataFrame())
            
            ratios = {}
            
            # ROE (Return on Equity)
            ratios['roe'] = info.get('returnOnEquity', None)
            if ratios['roe']:
                ratios['roe'] *= 100  # Convert to percentage
            
            # ROA (Return on Assets)
            ratios['roa'] = info.get('returnOnAssets', None)
            if ratios['roa']:
                ratios['roa'] *= 100  # Convert to percentage
            
            # Profit Margin
            ratios['profit_margin'] = info.get('profitMargins', None)
            if ratios['profit_margin']:
                ratios['profit_margin'] *= 100  # Convert to percentage
            
            # Operating Margin
            ratios['operating_margin'] = info.get('operatingMargins', None)
            if ratios['operating_margin']:
                ratios['operating_margin'] *= 100  # Convert to percentage
            
            # Gross Margin
            ratios['gross_margin'] = info.get('grossMargins', None)
            if ratios['gross_margin']:
                ratios['gross_margin'] *= 100  # Convert to percentage
            
            return ratios
            
        except Exception as e:
            self.logger.error(f"Error calculating profitability ratios: {str(e)}")
            return {}
    
    def calculate_financial_health_ratios(self, fundamental_data: Dict) -> Dict:
        """
        Tính toán các chỉ số sức khỏe tài chính
        
        Args:
            fundamental_data: Dữ liệu cơ bản
        
        Returns:
            Dictionary với các chỉ số sức khỏe tài chính
        """
        try:
            info = fundamental_data.get('info', {})
            balance_sheet = fundamental_data.get('balance_sheet', pd.DataFrame())
            
            ratios = {}
            
            # Debt-to-Equity Ratio
            ratios['debt_to_equity'] = info.get('debtToEquity', None)
            
            # Current Ratio
            ratios['current_ratio'] = info.get('currentRatio', None)
            
            # Quick Ratio
            ratios['quick_ratio'] = info.get('quickRatio', None)
            
            # Interest Coverage
            ratios['interest_coverage'] = info.get('interestCoverage', None)
            
            # Cash Ratio
            ratios['cash_ratio'] = info.get('cashRatio', None)
            
            return ratios
            
        except Exception as e:
            self.logger.error(f"Error calculating financial health ratios: {str(e)}")
            return {}
    
    def calculate_growth_metrics(self, fundamental_data: Dict) -> Dict:
        """
        Tính toán các chỉ số tăng trưởng
        
        Args:
            fundamental_data: Dữ liệu cơ bản
        
        Returns:
            Dictionary với các chỉ số tăng trưởng
        """
        try:
            info = fundamental_data.get('info', {})
            
            metrics = {}
            
            # Revenue Growth
            metrics['revenue_growth'] = info.get('revenueGrowth', None)
            if metrics['revenue_growth']:
                metrics['revenue_growth'] *= 100  # Convert to percentage
            
            # Earnings Growth
            metrics['earnings_growth'] = info.get('earningsGrowth', None)
            if metrics['earnings_growth']:
                metrics['earnings_growth'] *= 100  # Convert to percentage
            
            # EPS Growth
            metrics['eps_growth'] = info.get('earningsQuarterlyGrowth', None)
            if metrics['eps_growth']:
                metrics['eps_growth'] *= 100  # Convert to percentage
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating growth metrics: {str(e)}")
            return {}
    
    def generate_fundamental_report(self, symbol: str, market: str = "US") -> Dict:
        """
        Tạo báo cáo phân tích cơ bản toàn diện
        
        Args:
            symbol: Mã cổ phiếu
            market: Thị trường
        
        Returns:
            Dictionary với báo cáo phân tích cơ bản
        """
        try:
            # Lấy dữ liệu cơ bản
            fundamental_data = self.get_fundamental_data(symbol, market)
            
            if not fundamental_data:
                return {'error': f'Không thể lấy dữ liệu cơ bản cho {symbol}'}
            
            # Tính toán các chỉ số
            valuation_ratios = self.calculate_valuation_ratios(fundamental_data)
            profitability_ratios = self.calculate_profitability_ratios(fundamental_data)
            financial_health_ratios = self.calculate_financial_health_ratios(fundamental_data)
            growth_metrics = self.calculate_growth_metrics(fundamental_data)
            
            # Đánh giá tổng thể
            overall_score = self._calculate_overall_score(
                valuation_ratios, profitability_ratios, 
                financial_health_ratios, growth_metrics
            )
            
            # Khuyến nghị
            recommendation = self._generate_recommendation(overall_score)
            
            return {
                'symbol': symbol,
                'market': market,
                'valuation_ratios': valuation_ratios,
                'profitability_ratios': profitability_ratios,
                'financial_health_ratios': financial_health_ratios,
                'growth_metrics': growth_metrics,
                'overall_score': overall_score,
                'recommendation': recommendation,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"Error generating fundamental report for {symbol}: {str(e)}")
            return {'error': f'Lỗi khi tạo báo cáo cơ bản: {str(e)}'}
    
    def _calculate_overall_score(self, valuation_ratios: Dict, profitability_ratios: Dict, 
                                financial_health_ratios: Dict, growth_metrics: Dict) -> float:
        """Tính điểm tổng thể dựa trên các chỉ số"""
        score = 0.0
        total_weights = 0.0
        
        # Valuation Score (30%)
        if valuation_ratios.get('pe_ratio'):
            pe = valuation_ratios['pe_ratio']
            if pe and pe > 0:
                if pe <= self.thresholds['pe_good']:
                    score += 30
                elif pe <= self.thresholds['pe_high']:
                    score += 20
                else:
                    score += 10
                total_weights += 30
        
        # Profitability Score (25%)
        if profitability_ratios.get('roe'):
            roe = profitability_ratios['roe']
            if roe and roe > 0:
                if roe >= self.thresholds['roe_excellent']:
                    score += 25
                elif roe >= self.thresholds['roe_good']:
                    score += 20
                else:
                    score += 10
                total_weights += 25
        
        # Financial Health Score (25%)
        if financial_health_ratios.get('debt_to_equity'):
            debt_ratio = financial_health_ratios['debt_to_equity']
            if debt_ratio and debt_ratio > 0:
                if debt_ratio <= self.thresholds['debt_ratio_good']:
                    score += 25
                elif debt_ratio <= self.thresholds['debt_ratio_high']:
                    score += 15
                else:
                    score += 5
                total_weights += 25
        
        # Growth Score (20%)
        if growth_metrics.get('revenue_growth'):
            revenue_growth = growth_metrics['revenue_growth']
            if revenue_growth and revenue_growth > 0:
                if revenue_growth >= 20:
                    score += 20
                elif revenue_growth >= 10:
                    score += 15
                else:
                    score += 5
                total_weights += 20
        
        return (score / total_weights * 100) if total_weights > 0 else 0.0
    
    def _generate_recommendation(self, overall_score: float) -> str:
        """Tạo khuyến nghị dựa trên điểm tổng thể"""
        if overall_score >= 80:
            return "STRONG_BUY"
        elif overall_score >= 65:
            return "BUY"
        elif overall_score >= 50:
            return "HOLD"
        elif overall_score >= 35:
            return "SELL"
        else:
            return "STRONG_SELL"
