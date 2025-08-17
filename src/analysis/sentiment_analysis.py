"""
Market Sentiment Analysis Module
Phân tích tâm lý thị trường và sentiment
"""

import pandas as pd
import numpy as np
import requests
import json
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
import os

class SentimentAnalyzer:
    """Class phân tích sentiment thị trường"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # API Keys
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        # Sentiment thresholds
        self.sentiment_thresholds = {
            'very_bullish': 0.7,
            'bullish': 0.3,
            'neutral': 0.0,
            'bearish': -0.3,
            'very_bearish': -0.7
        }
    
    def get_news_sentiment(self, symbol: str, days: int = 7) -> Dict:
        """
        Lấy sentiment từ tin tức
        
        Args:
            symbol: Mã cổ phiếu
            days: Số ngày lấy dữ liệu
        
        Returns:
            Dictionary với sentiment data
        """
        try:
            if not self.news_api_key:
                return {'error': 'News API key not configured'}
            
            # Get news articles
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': f'"{symbol}" AND (stock OR market OR trading OR investment)',
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return {'error': f'News API error: {response.status_code}'}
            
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                return {'error': 'No news articles found'}
            
            # Analyze sentiment for each article
            sentiments = []
            for article in articles[:20]:  # Limit to 20 articles
                sentiment = self._analyze_article_sentiment(article)
                sentiments.append(sentiment)
            
            # Calculate overall sentiment
            overall_sentiment = np.mean(sentiments) if sentiments else 0
            
            return {
                'symbol': symbol,
                'articles_count': len(articles),
                'sentiments': sentiments,
                'overall_sentiment': overall_sentiment,
                'sentiment_label': self._get_sentiment_label(overall_sentiment),
                'articles': articles[:5]  # Return first 5 articles for reference
            }
            
        except Exception as e:
            self.logger.error(f"Error getting news sentiment for {symbol}: {str(e)}")
            return {'error': f'Error analyzing news sentiment: {str(e)}'}
    
    def _analyze_article_sentiment(self, article: Dict) -> float:
        """Phân tích sentiment của một bài báo"""
        try:
            # Simple keyword-based sentiment analysis
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = f"{title} {description}"
            
            # Bullish keywords
            bullish_words = [
                'bullish', 'surge', 'rally', 'gain', 'rise', 'up', 'positive',
                'growth', 'profit', 'earnings', 'beat', 'exceed', 'strong',
                'buy', 'upgrade', 'outperform', 'positive', 'optimistic'
            ]
            
            # Bearish keywords
            bearish_words = [
                'bearish', 'fall', 'drop', 'decline', 'down', 'negative',
                'loss', 'miss', 'weak', 'sell', 'downgrade', 'underperform',
                'negative', 'pessimistic', 'concern', 'risk', 'worry'
            ]
            
            # Count keywords
            bullish_count = sum(1 for word in bullish_words if word in content)
            bearish_count = sum(1 for word in bearish_words if word in content)
            
            # Calculate sentiment score (-1 to 1)
            total_words = bullish_count + bearish_count
            if total_words == 0:
                return 0.0
            
            sentiment_score = (bullish_count - bearish_count) / total_words
            return sentiment_score
            
        except Exception as e:
            self.logger.error(f"Error analyzing article sentiment: {str(e)}")
            return 0.0
    
    def get_market_breadth(self, market: str = "US") -> Dict:
        """
        Lấy market breadth indicators
        
        Args:
            market: Thị trường (US/VN)
        
        Returns:
            Dictionary với market breadth data
        """
        try:
            if market == "US":
                # US market breadth indicators
                indicators = {
                    'advancing': 0,
                    'declining': 0,
                    'unchanged': 0,
                    'advance_decline_ratio': 0.0,
                    'new_highs': 0,
                    'new_lows': 0,
                    'high_low_ratio': 0.0
                }
                
                # Placeholder - would need real market data
                # In real implementation, this would fetch from market data provider
                
                return indicators
            else:
                # VN market breadth
                return self._get_vn_market_breadth()
                
        except Exception as e:
            self.logger.error(f"Error getting market breadth: {str(e)}")
            return {'error': f'Error getting market breadth: {str(e)}'}
    
    def _get_vn_market_breadth(self) -> Dict:
        """Lấy market breadth cho thị trường VN"""
        # Placeholder implementation
        return {
            'advancing': 150,
            'declining': 100,
            'unchanged': 50,
            'advance_decline_ratio': 1.5,
            'new_highs': 20,
            'new_lows': 10,
            'high_low_ratio': 2.0
        }
    
    def get_economic_indicators(self) -> Dict:
        """
        Lấy các chỉ số kinh tế quan trọng
        
        Returns:
            Dictionary với economic indicators
        """
        try:
            # Placeholder - would fetch from economic data providers
            indicators = {
                'vix': 20.5,  # Volatility Index
                'usd_index': 95.2,  # US Dollar Index
                'gold_price': 1950.0,  # Gold price
                'oil_price': 75.0,  # Oil price
                'bond_yield_10y': 4.2,  # 10-year Treasury yield
                'fed_rate': 5.5,  # Federal Reserve rate
                'inflation_rate': 3.2,  # Inflation rate
                'unemployment_rate': 3.8  # Unemployment rate
            }
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error getting economic indicators: {str(e)}")
            return {'error': f'Error getting economic indicators: {str(e)}'}
    
    def get_sector_rotation(self, market: str = "US") -> Dict:
        """
        Phân tích sector rotation
        
        Args:
            market: Thị trường (US/VN)
        
        Returns:
            Dictionary với sector rotation data
        """
        try:
            if market == "US":
                sectors = {
                    'Technology': {'performance': 0.15, 'momentum': 'bullish'},
                    'Healthcare': {'performance': 0.08, 'momentum': 'neutral'},
                    'Financial': {'performance': 0.05, 'momentum': 'bearish'},
                    'Consumer_Discretionary': {'performance': 0.12, 'momentum': 'bullish'},
                    'Energy': {'performance': -0.03, 'momentum': 'bearish'},
                    'Industrials': {'performance': 0.06, 'momentum': 'neutral'},
                    'Materials': {'performance': 0.04, 'momentum': 'neutral'},
                    'Utilities': {'performance': -0.02, 'momentum': 'bearish'},
                    'Real_Estate': {'performance': 0.02, 'momentum': 'neutral'},
                    'Consumer_Staples': {'performance': 0.03, 'momentum': 'neutral'}
                }
            else:
                # VN market sectors
                sectors = {
                    'Banking': {'performance': 0.10, 'momentum': 'bullish'},
                    'Real_Estate': {'performance': 0.08, 'momentum': 'bullish'},
                    'Consumer': {'performance': 0.06, 'momentum': 'neutral'},
                    'Technology': {'performance': 0.12, 'momentum': 'bullish'},
                    'Materials': {'performance': 0.04, 'momentum': 'neutral'},
                    'Energy': {'performance': -0.02, 'momentum': 'bearish'},
                    'Industrials': {'performance': 0.05, 'momentum': 'neutral'},
                    'Healthcare': {'performance': 0.07, 'momentum': 'bullish'},
                    'Utilities': {'performance': 0.03, 'momentum': 'neutral'},
                    'Telecommunications': {'performance': 0.02, 'momentum': 'neutral'}
                }
            
            # Calculate sector rotation score
            total_performance = sum(sector['performance'] for sector in sectors.values())
            avg_performance = total_performance / len(sectors)
            
            # Determine rotation direction
            if avg_performance > 0.05:
                rotation_direction = 'risk_on'
            elif avg_performance < -0.02:
                rotation_direction = 'risk_off'
            else:
                rotation_direction = 'neutral'
            
            return {
                'sectors': sectors,
                'average_performance': avg_performance,
                'rotation_direction': rotation_direction,
                'top_performing_sectors': sorted(sectors.items(), 
                                               key=lambda x: x[1]['performance'], 
                                               reverse=True)[:3],
                'worst_performing_sectors': sorted(sectors.items(), 
                                                 key=lambda x: x[1]['performance'])[:3]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting sector rotation: {str(e)}")
            return {'error': f'Error getting sector rotation: {str(e)}'}
    
    def get_social_sentiment(self, symbol: str) -> Dict:
        """
        Lấy sentiment từ social media (placeholder)
        
        Args:
            symbol: Mã cổ phiếu
        
        Returns:
            Dictionary với social sentiment data
        """
        try:
            # Placeholder implementation
            # In real implementation, this would analyze Twitter, Reddit, etc.
            
            sentiment_data = {
                'symbol': symbol,
                'twitter_sentiment': 0.15,
                'reddit_sentiment': 0.08,
                'stocktwits_sentiment': 0.12,
                'overall_social_sentiment': 0.12,
                'social_volume': 1500,
                'sentiment_label': 'bullish'
            }
            
            return sentiment_data
            
        except Exception as e:
            self.logger.error(f"Error getting social sentiment for {symbol}: {str(e)}")
            return {'error': f'Error getting social sentiment: {str(e)}'}
    
    def generate_market_sentiment_report(self, symbol: str = None, market: str = "US") -> Dict:
        """
        Tạo báo cáo sentiment thị trường toàn diện
        
        Args:
            symbol: Mã cổ phiếu (optional)
            market: Thị trường
        
        Returns:
            Dictionary với báo cáo sentiment
        """
        try:
            report = {
                'market': market,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'overall_sentiment': 'neutral'
            }
            
            # News sentiment
            if symbol:
                news_sentiment = self.get_news_sentiment(symbol)
                report['news_sentiment'] = news_sentiment
            
            # Market breadth
            market_breadth = self.get_market_breadth(market)
            report['market_breadth'] = market_breadth
            
            # Economic indicators
            economic_indicators = self.get_economic_indicators()
            report['economic_indicators'] = economic_indicators
            
            # Sector rotation
            sector_rotation = self.get_sector_rotation(market)
            report['sector_rotation'] = sector_rotation
            
            # Social sentiment
            if symbol:
                social_sentiment = self.get_social_sentiment(symbol)
                report['social_sentiment'] = social_sentiment
            
            # Calculate overall market sentiment
            overall_sentiment = self._calculate_overall_market_sentiment(report)
            report['overall_sentiment'] = overall_sentiment
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating market sentiment report: {str(e)}")
            return {'error': f'Error generating market sentiment report: {str(e)}'}
    
    def _calculate_overall_market_sentiment(self, report: Dict) -> str:
        """Tính toán sentiment tổng thể của thị trường"""
        try:
            sentiment_scores = []
            
            # News sentiment score
            if 'news_sentiment' in report and 'overall_sentiment' in report['news_sentiment']:
                news_score = report['news_sentiment']['overall_sentiment']
                sentiment_scores.append(news_score)
            
            # Market breadth score
            if 'market_breadth' in report and 'advance_decline_ratio' in report['market_breadth']:
                ad_ratio = report['market_breadth']['advance_decline_ratio']
                if ad_ratio > 1.2:
                    breadth_score = 0.3
                elif ad_ratio > 1.0:
                    breadth_score = 0.1
                elif ad_ratio < 0.8:
                    breadth_score = -0.3
                else:
                    breadth_score = -0.1
                sentiment_scores.append(breadth_score)
            
            # Economic indicators score
            if 'economic_indicators' in report:
                vix = report['economic_indicators'].get('vix', 20)
                if vix < 15:
                    vix_score = 0.2  # Low volatility = bullish
                elif vix > 30:
                    vix_score = -0.2  # High volatility = bearish
                else:
                    vix_score = 0.0
                sentiment_scores.append(vix_score)
            
            # Sector rotation score
            if 'sector_rotation' in report:
                rotation = report['sector_rotation'].get('rotation_direction', 'neutral')
                if rotation == 'risk_on':
                    rotation_score = 0.2
                elif rotation == 'risk_off':
                    rotation_score = -0.2
                else:
                    rotation_score = 0.0
                sentiment_scores.append(rotation_score)
            
            # Calculate overall sentiment
            if sentiment_scores:
                overall_score = np.mean(sentiment_scores)
                return self._get_sentiment_label(overall_score)
            else:
                return 'neutral'
                
        except Exception as e:
            self.logger.error(f"Error calculating overall market sentiment: {str(e)}")
            return 'neutral'
    
    def _get_sentiment_label(self, score: float) -> str:
        """Chuyển đổi sentiment score thành label"""
        if score >= self.sentiment_thresholds['very_bullish']:
            return 'very_bullish'
        elif score >= self.sentiment_thresholds['bullish']:
            return 'bullish'
        elif score >= self.sentiment_thresholds['neutral']:
            return 'neutral'
        elif score >= self.sentiment_thresholds['bearish']:
            return 'bearish'
        else:
            return 'very_bearish'
