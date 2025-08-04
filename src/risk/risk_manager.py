"""
Risk Management Module
Quản lý rủi ro và portfolio optimization
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

class RiskManager:
    """Class quản lý rủi ro"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.logger = logging.getLogger(__name__)
        self.risk_free_rate = risk_free_rate
    
    def calculate_returns(self, prices: pd.Series) -> pd.Series:
        """
        Tính toán returns
        
        Args:
            prices: Series giá
        
        Returns:
            Series returns
        """
        return prices.pct_change().dropna()
    
    def calculate_volatility(self, returns: pd.Series, window: int = 252) -> pd.Series:
        """
        Tính toán volatility (độ biến động)
        
        Args:
            returns: Series returns
            window: Cửa sổ tính toán (ngày)
        
        Returns:
            Series volatility
        """
        return returns.rolling(window=window).std() * np.sqrt(252)
    
    def calculate_var(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """
        Tính Value at Risk (VaR)
        
        Args:
            returns: Series returns
            confidence_level: Mức độ tin cậy (default 5%)
        
        Returns:
            VaR value
        """
        return np.percentile(returns, confidence_level * 100)
    
    def calculate_cvar(self, returns: pd.Series, confidence_level: float = 0.05) -> float:
        """
        Tính Conditional Value at Risk (CVaR) / Expected Shortfall
        
        Args:
            returns: Series returns
            confidence_level: Mức độ tin cậy
        
        Returns:
            CVaR value
        """
        var = self.calculate_var(returns, confidence_level)
        return returns[returns <= var].mean()
    
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = None) -> float:
        """
        Tính Sharpe Ratio
        
        Args:
            returns: Series returns
            risk_free_rate: Risk-free rate
        
        Returns:
            Sharpe ratio
        """
        if risk_free_rate is None:
            risk_free_rate = self.risk_free_rate
        
        excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
        return excess_returns.mean() / returns.std() * np.sqrt(252)
    
    def calculate_sortino_ratio(self, returns: pd.Series, risk_free_rate: float = None) -> float:
        """
        Tính Sortino Ratio (chỉ xem xét downside risk)
        
        Args:
            returns: Series returns
            risk_free_rate: Risk-free rate
        
        Returns:
            Sortino ratio
        """
        if risk_free_rate is None:
            risk_free_rate = self.risk_free_rate
        
        excess_returns = returns - risk_free_rate / 252
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0:
            return np.inf
        
        downside_deviation = np.sqrt(np.mean(downside_returns**2))
        return excess_returns.mean() / downside_deviation * np.sqrt(252)
    
    def calculate_max_drawdown(self, prices: pd.Series) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
        """
        Tính Maximum Drawdown
        
        Args:
            prices: Series giá
        
        Returns:
            Tuple (max_drawdown, start_date, end_date)
        """
        cumulative = prices / prices.iloc[0]
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = drawdown.min()
        end_date = drawdown.idxmin()
        
        # Tìm start date
        peak = running_max.loc[:end_date].idxmax()
        
        return max_dd, peak, end_date
    
    def calculate_beta(self, asset_returns: pd.Series, market_returns: pd.Series) -> float:
        """
        Tính Beta (độ nhạy với thị trường)
        
        Args:
            asset_returns: Returns của asset
            market_returns: Returns của thị trường
        
        Returns:
            Beta value
        """
        # Align data
        aligned_data = pd.concat([asset_returns, market_returns], axis=1).dropna()
        if len(aligned_data) < 30:
            return 1.0
        
        asset_ret = aligned_data.iloc[:, 0]
        market_ret = aligned_data.iloc[:, 1]
        
        covariance = np.cov(asset_ret, market_ret)[0, 1]
        market_variance = np.var(market_ret)
        
        return covariance / market_variance if market_variance != 0 else 1.0
    
    def calculate_correlation_matrix(self, returns_data: pd.DataFrame) -> pd.DataFrame:
        """
        Tính correlation matrix
        
        Args:
            returns_data: DataFrame với returns của nhiều assets
        
        Returns:
            Correlation matrix
        """
        return returns_data.corr()
    
    def optimize_portfolio(self, returns_data: pd.DataFrame, method: str = 'sharpe') -> Dict:
        """
        Tối ưu hóa portfolio
        
        Args:
            returns_data: DataFrame với returns của các assets
            method: Phương pháp tối ưu ('sharpe', 'min_variance', 'equal_weight')
        
        Returns:
            Dictionary với weights và metrics
        """
        n_assets = len(returns_data.columns)
        
        if method == 'equal_weight':
            weights = np.array([1/n_assets] * n_assets)
        else:
            # Tính covariance matrix
            cov_matrix = returns_data.cov() * 252  # Annualized
            
            if method == 'min_variance':
                # Minimize variance
                def objective(weights):
                    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                
                constraints = [
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
                ]
                bounds = tuple((0, 1) for _ in range(n_assets))  # Weights between 0 and 1
                
                result = minimize(objective, [1/n_assets] * n_assets, 
                                method='SLSQP', bounds=bounds, constraints=constraints)
                weights = result.x
                
            elif method == 'sharpe':
                # Maximize Sharpe ratio
                mean_returns = returns_data.mean() * 252  # Annualized
                
                def objective(weights):
                    portfolio_return = np.sum(mean_returns * weights)
                    portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                    return -(portfolio_return - self.risk_free_rate) / portfolio_vol
                
                constraints = [
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
                ]
                bounds = tuple((0, 1) for _ in range(n_assets))
                
                result = minimize(objective, [1/n_assets] * n_assets,
                                method='SLSQP', bounds=bounds, constraints=constraints)
                weights = result.x
        
        # Calculate portfolio metrics
        portfolio_returns = returns_data.dot(weights)
        portfolio_mean = portfolio_returns.mean() * 252
        portfolio_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (portfolio_mean - self.risk_free_rate) / portfolio_vol
        
        return {
            'weights': dict(zip(returns_data.columns, weights)),
            'portfolio_return': portfolio_mean,
            'portfolio_volatility': portfolio_vol,
            'sharpe_ratio': sharpe_ratio,
            'method': method
        }
    
    def calculate_position_size(self, capital: float, risk_per_trade: float, 
                              stop_loss_pct: float, current_price: float) -> float:
        """
        Tính toán kích thước position dựa trên risk management
        
        Args:
            capital: Tổng vốn
            risk_per_trade: % rủi ro cho mỗi giao dịch
            stop_loss_pct: % stop loss
            current_price: Giá hiện tại
        
        Returns:
            Số lượng shares/units
        """
        risk_amount = capital * risk_per_trade
        stop_loss_amount = current_price * stop_loss_pct
        
        if stop_loss_amount == 0:
            return 0
        
        position_size = risk_amount / stop_loss_amount
        return position_size
    
    def generate_risk_report(self, data: pd.DataFrame, symbol: str) -> Dict:
        """
        Tạo báo cáo rủi ro cho một asset
        
        Args:
            data: DataFrame với dữ liệu OHLCV
            symbol: Mã symbol
        
        Returns:
            Dictionary với các metrics rủi ro
        """
        returns = self.calculate_returns(data['Close'])
        
        if len(returns) < 30:
            return {"error": "Không đủ dữ liệu để tính toán rủi ro"}
        
        # Basic metrics
        volatility = self.calculate_volatility(returns)
        var_95 = self.calculate_var(returns, 0.05)
        var_99 = self.calculate_var(returns, 0.01)
        cvar_95 = self.calculate_cvar(returns, 0.05)
        sharpe = self.calculate_sharpe_ratio(returns)
        sortino = self.calculate_sortino_ratio(returns)
        max_dd, dd_start, dd_end = self.calculate_max_drawdown(data['Close'])
        
        # Current metrics
        current_vol = volatility.iloc[-1] if not volatility.empty else 0
        current_price = data['Close'].iloc[-1]
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'volatility_annual': current_vol,
            'var_95': var_95,
            'var_99': var_99,
            'cvar_95': cvar_95,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'max_drawdown': max_dd,
            'max_drawdown_start': dd_start,
            'max_drawdown_end': dd_end,
            'total_return': (current_price / data['Close'].iloc[0] - 1) * 100,
            'analysis_date': datetime.now()
        }
    
    def get_risk_alerts(self, data: pd.DataFrame, symbol: str, 
                       volatility_threshold: float = 0.3,
                       drawdown_threshold: float = -0.1) -> List[Dict]:
        """
        Tạo cảnh báo rủi ro
        
        Args:
            data: DataFrame với dữ liệu
            symbol: Mã symbol
            volatility_threshold: Ngưỡng volatility
            drawdown_threshold: Ngưỡng drawdown
        
        Returns:
            List các cảnh báo
        """
        alerts = []
        returns = self.calculate_returns(data['Close'])
        
        if len(returns) < 30:
            return alerts
        
        # Volatility alert
        current_vol = self.calculate_volatility(returns).iloc[-1]
        if current_vol > volatility_threshold:
            alerts.append({
                'type': 'HIGH_VOLATILITY',
                'message': f'Volatility cao: {current_vol:.2%}',
                'severity': 'WARNING',
                'date': datetime.now()
            })
        
        # Drawdown alert
        current_dd, _, _ = self.calculate_max_drawdown(data['Close'])
        if current_dd < drawdown_threshold:
            alerts.append({
                'type': 'HIGH_DRAWDOWN',
                'message': f'Drawdown cao: {current_dd:.2%}',
                'severity': 'CRITICAL',
                'date': datetime.now()
            })
        
        # VaR alert
        var_95 = self.calculate_var(returns, 0.05)
        if var_95 < -0.02:  # VaR > 2%
            alerts.append({
                'type': 'HIGH_VAR',
                'message': f'VaR cao: {var_95:.2%}',
                'severity': 'WARNING',
                'date': datetime.now()
            })
        
        return alerts

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test risk manager
    from src.data.data_collector import DataCollector
    
    collector = DataCollector()
    risk_manager = RiskManager()
    
    # Lấy dữ liệu
    data = collector.get_stock_data("AAPL", period="1y")
    if not data.empty:
        # Tạo báo cáo rủi ro
        risk_report = risk_manager.generate_risk_report(data, "AAPL")
        print("Risk Report:", risk_report)
        
        # Tạo cảnh báo
        alerts = risk_manager.get_risk_alerts(data, "AAPL")
        print("Risk Alerts:", alerts)
        
        # Test portfolio optimization với nhiều assets
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]
        returns_data = pd.DataFrame()
        
        for symbol in symbols:
            symbol_data = collector.get_stock_data(symbol, period="1y")
            if not symbol_data.empty:
                returns_data[symbol] = risk_manager.calculate_returns(symbol_data['Close'])
        
        if len(returns_data.columns) > 1:
            # Tối ưu portfolio
            portfolio = risk_manager.optimize_portfolio(returns_data, 'sharpe')
            print("Portfolio Optimization:", portfolio) 