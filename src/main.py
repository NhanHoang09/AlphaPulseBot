"""
FinGPT Main Application
Bot phân tích và dự báo xu hướng tài chính
"""

import logging
import schedule
import time
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from src.risk.risk_manager import RiskManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fingpt.log'),
        logging.StreamHandler()
    ]
)

class FinGPTBot:
    """Main bot class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.predictor = PredictionModels()
        self.risk_manager = RiskManager()
        
        # Configuration
        self.symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        self.analysis_interval = 60  # minutes
        
        self.logger.info("FinGPT Bot initialized")
    
    def analyze_symbol(self, symbol: str):
        """Phân tích một symbol"""
        try:
            self.logger.info(f"Analyzing {symbol}")
            
            # Get data
            data = self.collector.get_stock_data(symbol, period="6mo")
            if data.empty:
                self.logger.warning(f"No data available for {symbol}")
                return
            
            # Technical analysis
            data_with_indicators = self.analyzer.add_all_indicators(data)
            signals = self.analyzer.get_trading_signals(data_with_indicators)
            
            # Risk analysis
            risk_report = self.risk_manager.generate_risk_report(data, symbol)
            risk_alerts = self.risk_manager.get_risk_alerts(data, symbol)
            
            # AI prediction
            prediction = self.predictor.predict(data, symbol, 'lstm')
            
            # Log results
            self.logger.info(f"{symbol} Analysis Results:")
            self.logger.info(f"  Trading Signals: {signals}")
            self.logger.info(f"  Risk Report: {risk_report}")
            self.logger.info(f"  Prediction: {prediction}")
            
            if risk_alerts:
                self.logger.warning(f"  Risk Alerts: {risk_alerts}")
            
            # Save data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/analysis_{symbol}_{timestamp}.csv"
            data_with_indicators.to_csv(filename)
            
        except Exception as e:
            self.logger.error(f"Error analyzing {symbol}: {str(e)}")
    
    def run_analysis(self):
        """Chạy phân tích cho tất cả symbols"""
        self.logger.info("Starting analysis run")
        
        for symbol in self.symbols:
            self.analyze_symbol(symbol)
            time.sleep(1)  # Avoid rate limiting
        
        self.logger.info("Analysis run completed")
    
    def train_models(self):
        """Training các models"""
        self.logger.info("Starting model training")
        
        for symbol in self.symbols:
            try:
                data = self.collector.get_stock_data(symbol, period="2y")
                if not data.empty:
                    # Train LSTM model
                    lstm_result = self.predictor.train_lstm_model(data, symbol)
                    if 'error' not in lstm_result:
                        self.logger.info(f"LSTM model trained for {symbol}")
                    
                    # Train ensemble model
                    ensemble_result = self.predictor.train_ensemble_model(data, symbol)
                    if 'error' not in ensemble_result:
                        self.logger.info(f"Ensemble model trained for {symbol}")
                
                time.sleep(2)  # Avoid rate limiting
                
            except Exception as e:
                self.logger.error(f"Error training models for {symbol}: {str(e)}")
        
        self.logger.info("Model training completed")
    
    def generate_daily_report(self):
        """Tạo báo cáo hàng ngày"""
        self.logger.info("Generating daily report")
        
        report = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'symbols_analyzed': [],
            'signals': {},
            'risk_alerts': [],
            'predictions': {}
        }
        
        for symbol in self.symbols:
            try:
                data = self.collector.get_stock_data(symbol, period="1mo")
                if not data.empty:
                    # Technical analysis
                    data_with_indicators = self.analyzer.add_all_indicators(data)
                    signals = self.analyzer.get_trading_signals(data_with_indicators)
                    
                    # Risk analysis
                    risk_alerts = self.risk_manager.get_risk_alerts(data, symbol)
                    
                    # Prediction
                    prediction = self.predictor.predict(data, symbol, 'lstm')
                    
                    # Add to report
                    report['symbols_analyzed'].append(symbol)
                    report['signals'][symbol] = signals
                    report['predictions'][symbol] = prediction
                    
                    if risk_alerts:
                        report['risk_alerts'].extend(risk_alerts)
                
            except Exception as e:
                self.logger.error(f"Error generating report for {symbol}: {str(e)}")
        
        # Save report
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"data/daily_report_{timestamp}.json"
        
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Daily report saved to {report_filename}")
        return report
    
    def schedule_tasks(self):
        """Lên lịch các tác vụ"""
        # Run analysis every hour
        schedule.every(self.analysis_interval).minutes.do(self.run_analysis)
        
        # Train models daily at 2 AM
        schedule.every().day.at("02:00").do(self.train_models)
        
        # Generate daily report at 6 PM
        schedule.every().day.at("18:00").do(self.generate_daily_report)
        
        self.logger.info("Tasks scheduled")
    
    def run(self):
        """Chạy bot"""
        self.logger.info("Starting FinGPT Bot")
        
        # Schedule tasks
        self.schedule_tasks()
        
        # Run initial analysis
        self.run_analysis()
        
        # Main loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Bot error: {str(e)}")

def main():
    """Main function"""
    print("🤖 FinGPT - AI Trading Bot")
    print("=" * 50)
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Initialize bot
    bot = FinGPTBot()
    
    # Run bot
    bot.run()

if __name__ == "__main__":
    main() 