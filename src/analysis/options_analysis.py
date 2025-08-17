"""
Options Analysis Module
Phân tích options với Greeks và IV analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
from scipy.stats import norm

class OptionsAnalyzer:
    """Class phân tích options"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Risk-free rate (annual)
        self.risk_free_rate = 0.05
        
        # Greeks calculation parameters
        self.delta_step = 0.01
        self.gamma_step = 0.01
        self.theta_step = 1/365  # 1 day
        self.vega_step = 0.01
    
    def calculate_black_scholes(self, S: float, K: float, T: float, r: float, 
                              sigma: float, option_type: str = 'call') -> Dict:
        """
        Tính toán Black-Scholes option pricing
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            sigma: Volatility
            option_type: 'call' or 'put'
        
        Returns:
            Dictionary với option price và Greeks
        """
        try:
            if T <= 0:
                return {'error': 'Time to expiration must be positive'}
            
            # Calculate d1 and d2
            d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
            d2 = d1 - sigma*np.sqrt(T)
            
            # Calculate option price
            if option_type.lower() == 'call':
                price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
                delta = norm.cdf(d1)
                theta = (-S*sigma*norm.pdf(d1))/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2)
            else:  # put
                price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
                delta = norm.cdf(d1) - 1
                theta = (-S*sigma*norm.pdf(d1))/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2)
            
            # Calculate other Greeks
            gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T))
            vega = S*np.sqrt(T)*norm.pdf(d1)
            rho = K*T*np.exp(-r*T)*norm.cdf(d2) if option_type.lower() == 'call' else -K*T*np.exp(-r*T)*norm.cdf(-d2)
            
            return {
                'price': price,
                'delta': delta,
                'gamma': gamma,
                'theta': theta,
                'vega': vega,
                'rho': rho,
                'd1': d1,
                'd2': d2,
                'intrinsic_value': max(0, S-K) if option_type.lower() == 'call' else max(0, K-S),
                'time_value': price - max(0, S-K) if option_type.lower() == 'call' else price - max(0, K-S)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating Black-Scholes: {str(e)}")
            return {'error': f'Black-Scholes calculation error: {str(e)}'}
    
    def calculate_implied_volatility(self, S: float, K: float, T: float, r: float, 
                                   option_price: float, option_type: str = 'call', 
                                   tolerance: float = 0.0001, max_iterations: int = 100) -> float:
        """
        Tính toán Implied Volatility bằng Newton-Raphson method
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            option_price: Market price of option
            option_type: 'call' or 'put'
            tolerance: Convergence tolerance
            max_iterations: Maximum iterations
        
        Returns:
            Implied volatility
        """
        try:
            # Initial guess for volatility
            sigma = 0.3
            
            for i in range(max_iterations):
                # Calculate option price with current sigma
                result = self.calculate_black_scholes(S, K, T, r, sigma, option_type)
                
                if 'error' in result:
                    return None
                
                price = result['price']
                vega = result['vega']
                
                # Check convergence
                if abs(price - option_price) < tolerance:
                    return sigma
                
                # Update sigma using Newton-Raphson
                sigma = sigma - (price - option_price) / vega
                
                # Ensure sigma is positive
                sigma = max(0.001, sigma)
            
            return None  # Did not converge
            
        except Exception as e:
            self.logger.error(f"Error calculating implied volatility: {str(e)}")
            return None
    
    def analyze_options_chain(self, stock_price: float, options_data: List[Dict]) -> Dict:
        """
        Phân tích options chain
        
        Args:
            stock_price: Current stock price
            options_data: List of options data
        
        Returns:
            Dictionary với options chain analysis
        """
        try:
            analysis = {
                'stock_price': stock_price,
                'call_options': [],
                'put_options': [],
                'put_call_ratio': 0.0,
                'iv_skew': 0.0,
                'iv_term_structure': {},
                'max_pain': 0.0
            }
            
            calls = []
            puts = []
            
            for option in options_data:
                # Calculate implied volatility
                iv = self.calculate_implied_volatility(
                    stock_price,
                    option['strike'],
                    option['time_to_expiry'],
                    self.risk_free_rate,
                    option['price'],
                    option['type']
                )
                
                # Calculate Greeks
                greeks = self.calculate_black_scholes(
                    stock_price,
                    option['strike'],
                    option['time_to_expiry'],
                    self.risk_free_rate,
                    iv if iv else 0.3,
                    option['type']
                )
                
                option_analysis = {
                    'strike': option['strike'],
                    'expiry': option['expiry'],
                    'price': option['price'],
                    'volume': option.get('volume', 0),
                    'open_interest': option.get('open_interest', 0),
                    'implied_volatility': iv,
                    'delta': greeks.get('delta', 0),
                    'gamma': greeks.get('gamma', 0),
                    'theta': greeks.get('theta', 0),
                    'vega': greeks.get('vega', 0),
                    'intrinsic_value': greeks.get('intrinsic_value', 0),
                    'time_value': greeks.get('time_value', 0)
                }
                
                if option['type'].lower() == 'call':
                    calls.append(option_analysis)
                else:
                    puts.append(option_analysis)
            
            analysis['call_options'] = calls
            analysis['put_options'] = puts
            
            # Calculate Put-Call Ratio
            total_call_volume = sum(c['volume'] for c in calls)
            total_put_volume = sum(p['volume'] for p in puts)
            analysis['put_call_ratio'] = total_put_volume / total_call_volume if total_call_volume > 0 else 0
            
            # Calculate IV Skew (difference between ATM and OTM IV)
            atm_calls = [c for c in calls if abs(c['strike'] - stock_price) / stock_price < 0.05]
            otm_calls = [c for c in calls if c['strike'] > stock_price * 1.05]
            
            if atm_calls and otm_calls:
                atm_iv = np.mean([c['implied_volatility'] for c in atm_calls if c['implied_volatility']])
                otm_iv = np.mean([c['implied_volatility'] for c in otm_calls if c['implied_volatility']])
                analysis['iv_skew'] = otm_iv - atm_iv if atm_iv and otm_iv else 0
            
            # Calculate Max Pain (simplified)
            strikes = list(set([o['strike'] for o in options_data]))
            max_pain = min(strikes, key=lambda x: self._calculate_pain_at_strike(x, options_data))
            analysis['max_pain'] = max_pain
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing options chain: {str(e)}")
            return {'error': f'Options chain analysis error: {str(e)}'}
    
    def _calculate_pain_at_strike(self, strike: float, options_data: List[Dict]) -> float:
        """Tính toán pain tại một strike price"""
        try:
            total_pain = 0
            
            for option in options_data:
                if option['type'].lower() == 'call':
                    if strike > option['strike']:
                        total_pain += (strike - option['strike']) * option.get('open_interest', 0)
                else:  # put
                    if strike < option['strike']:
                        total_pain += (option['strike'] - strike) * option.get('open_interest', 0)
            
            return total_pain
            
        except Exception as e:
            self.logger.error(f"Error calculating pain at strike: {str(e)}")
            return 0
    
    def calculate_options_flow(self, options_data: List[Dict]) -> Dict:
        """
        Phân tích options flow
        
        Args:
            options_data: List of options data with volume and open interest
        
        Returns:
            Dictionary với options flow analysis
        """
        try:
            flow_analysis = {
                'total_volume': 0,
                'total_open_interest': 0,
                'call_volume': 0,
                'put_volume': 0,
                'unusual_activity': [],
                'flow_sentiment': 'neutral'
            }
            
            for option in options_data:
                volume = option.get('volume', 0)
                oi = option.get('open_interest', 0)
                
                flow_analysis['total_volume'] += volume
                flow_analysis['total_open_interest'] += oi
                
                if option['type'].lower() == 'call':
                    flow_analysis['call_volume'] += volume
                else:
                    flow_analysis['put_volume'] += volume
                
                # Detect unusual activity (volume > 2x average)
                if volume > 0 and oi > 0:
                    volume_oi_ratio = volume / oi
                    if volume_oi_ratio > 2.0:
                        flow_analysis['unusual_activity'].append({
                            'strike': option['strike'],
                            'type': option['type'],
                            'volume': volume,
                            'open_interest': oi,
                            'ratio': volume_oi_ratio
                        })
            
            # Determine flow sentiment
            if flow_analysis['call_volume'] > flow_analysis['put_volume'] * 1.5:
                flow_analysis['flow_sentiment'] = 'bullish'
            elif flow_analysis['put_volume'] > flow_analysis['call_volume'] * 1.5:
                flow_analysis['flow_sentiment'] = 'bearish'
            else:
                flow_analysis['flow_sentiment'] = 'neutral'
            
            return flow_analysis
            
        except Exception as e:
            self.logger.error(f"Error calculating options flow: {str(e)}")
            return {'error': f'Options flow calculation error: {str(e)}'}
    
    def generate_options_report(self, stock_price: float, options_data: List[Dict]) -> Dict:
        """
        Tạo báo cáo options toàn diện
        
        Args:
            stock_price: Current stock price
            options_data: List of options data
        
        Returns:
            Dictionary với báo cáo options
        """
        try:
            # Options chain analysis
            chain_analysis = self.analyze_options_chain(stock_price, options_data)
            
            # Options flow analysis
            flow_analysis = self.calculate_options_flow(options_data)
            
            # Combine analyses
            report = {
                'stock_price': stock_price,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'chain_analysis': chain_analysis,
                'flow_analysis': flow_analysis,
                'summary': {
                    'put_call_ratio': chain_analysis.get('put_call_ratio', 0),
                    'iv_skew': chain_analysis.get('iv_skew', 0),
                    'max_pain': chain_analysis.get('max_pain', 0),
                    'flow_sentiment': flow_analysis.get('flow_sentiment', 'neutral'),
                    'unusual_activity_count': len(flow_analysis.get('unusual_activity', []))
                }
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating options report: {str(e)}")
            return {'error': f'Options report generation error: {str(e)}'}
