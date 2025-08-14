"""
Batch Trainer Module
Train LSTM models cho tất cả các mã cổ phiếu trong danh sách và đánh giá hiệu quả
"""

import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime
from typing import Dict, List, Any
import json

from src.data.data_collector import DataCollector
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.ml.prediction_models import PredictionModels
from .report_generator import ReportGenerator
from .detailed_report_generator import DetailedReportGenerator

class BatchTrainer:
    """Class để train model cho nhiều mã cổ phiếu cùng lúc"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.predictor = PredictionModels()
        self.report_generator = ReportGenerator()
        self.detailed_report_generator = DetailedReportGenerator()
        
        # Tạo thư mục lưu kết quả
        os.makedirs("results", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def extract_stock_symbols(self, file_path: str = "data/top_10_data.md") -> Dict[str, List[str]]:
        """Trích xuất danh sách mã cổ phiếu từ file markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sectors = {}
            current_sector = None
            
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                
                # Tìm tên ngành
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and 'NGÀNH' in line:
                    current_sector = line.split('NGÀNH')[1].split('-')[0].strip()
                    sectors[current_sector] = []
                
                # Tìm mã cổ phiếu
                elif current_sector and ' - ' in line and len(line.split(' - ')[0]) <= 5:
                    symbol = line.split(' - ')[0].strip()
                    if symbol and not symbol.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                        sectors[current_sector].append(symbol)
            
            sectors = {k: v for k, v in sectors.items() if v}
            self.logger.info(f"Extracted {sum(len(v) for v in sectors.values())} symbols from {len(sectors)} sectors")
            return sectors
            
        except Exception as e:
            self.logger.error(f"Error extracting stock symbols: {str(e)}")
            return {}
    
    def train_single_stock(self, symbol: str, sector: str) -> Dict[str, Any]:
        """Train model cho một mã cổ phiếu"""
        try:
            self.logger.info(f"Starting training for {symbol} ({sector})")
            start_time = datetime.now()
            
            # Lấy dữ liệu
            data = self.collector.get_stock_data(symbol, period="2y")
            
            if data.empty:
                return {
                    'symbol': symbol,
                    'sector': sector,
                    'status': 'failed',
                    'error': 'No data available',
                    'training_time': 0
                }
            
            # Thêm technical indicators
            data_with_indicators = self.analyzer.add_all_indicators(data)
            
            if data_with_indicators.empty:
                return {
                    'symbol': symbol,
                    'sector': sector,
                    'status': 'failed',
                    'error': 'Failed to add indicators',
                    'training_time': 0
                }
            
            # Train LSTM model
            result = self.predictor.train_lstm_model(
                data_with_indicators, 
                symbol, 
                lookback=30, 
                prediction_horizon=1,
                epochs=50,
                batch_size=16
            )
            
            training_time = (datetime.now() - start_time).total_seconds()
            
            if 'error' in result:
                return {
                    'symbol': symbol,
                    'sector': sector,
                    'status': 'failed',
                    'error': result['error'],
                    'training_time': training_time
                }
            
            result.update({
                'symbol': symbol,
                'sector': sector,
                'status': 'success',
                'training_time': training_time,
                'data_points': len(data_with_indicators)
            })
            
            # Tạo console report
            console_report = self.detailed_report_generator.create_console_report(result)
            self.logger.info(f"Completed training for {symbol} - R²: {result.get('r2', 'N/A'):.4f}")
            print(f"\n{console_report}\n")
            return result
            
        except Exception as e:
            self.logger.error(f"Error training {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'sector': sector,
                'status': 'failed',
                'error': str(e),
                'training_time': 0
            }
    
    def train_all_stocks(self, file_path: str = "data/top_10_data.md") -> Dict[str, Any]:
        """Train model cho tất cả các mã cổ phiếu"""
        sectors = self.extract_stock_symbols(file_path)
        
        if not sectors:
            return {"error": "No sectors found"}
        
        # Tạo danh sách tất cả các mã cổ phiếu
        all_symbols = []
        for sector, symbols in sectors.items():
            for symbol in symbols:
                all_symbols.append((symbol, sector))
        
        self.logger.info(f"Starting batch training for {len(all_symbols)} symbols")
        
        # Khởi tạo detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_generator.start_report(timestamp)
        self.detailed_report_generator.start_report(timestamp)
        
        results = []
        successful_count = 0
        failed_count = 0
        
        # Train từng mã cổ phiếu
        for i, (symbol, sector) in enumerate(all_symbols, 1):
            self.logger.info(f"Progress: {i}/{len(all_symbols)} - Training {symbol}")
            
            result = self.train_single_stock(symbol, sector)
            results.append(result)
            
            # Thêm kết quả vào detailed report
            self.report_generator.add_stock_result(result)
            self.detailed_report_generator.add_stock_result(result)
            
            if result['status'] == 'success':
                successful_count += 1
            else:
                failed_count += 1
        
        # Tạo báo cáo tổng hợp
        summary = self.create_training_summary(results, sectors)
        
        # Thêm summary vào detailed report
        self.report_generator.add_summary(summary)
        self.detailed_report_generator.add_summary(summary)
        
        # Lưu kết quả
        self.save_results(results, summary)
        
        # Thêm đường dẫn report vào kết quả
        report_path = self.report_generator.get_report_path()
        detailed_report_path = self.detailed_report_generator.get_report_path()
        
        return {
            'summary': summary,
            'detailed_results': results,
            'total_symbols': len(all_symbols),
            'successful': successful_count,
            'failed': failed_count,
            'detailed_report_path': report_path,
            'detailed_markdown_report_path': detailed_report_path
        }
    
    def create_training_summary(self, results: List[Dict], sectors: Dict[str, List[str]]) -> Dict[str, Any]:
        """Tạo báo cáo tổng hợp về hiệu quả training"""
        # Phân tích theo ngành
        sector_analysis = {}
        for sector in sectors.keys():
            sector_results = [r for r in results if r['sector'] == sector]
            successful = [r for r in sector_results if r['status'] == 'success']
            
            if successful:
                r2_scores = [r.get('r2', 0) for r in successful]
                mse_scores = [r.get('mse', 0) for r in successful]
                training_times = [r.get('training_time', 0) for r in successful]
                
                sector_analysis[sector] = {
                    'total_symbols': len(sector_results),
                    'successful': len(successful),
                    'success_rate': len(successful) / len(sector_results),
                    'avg_r2': np.mean(r2_scores),
                    'max_r2': np.max(r2_scores),
                    'min_r2': np.min(r2_scores),
                    'avg_mse': np.mean(mse_scores),
                    'avg_training_time': np.mean(training_times),
                    'best_symbol': successful[np.argmax(r2_scores)]['symbol']
                }
            else:
                sector_analysis[sector] = {
                    'total_symbols': len(sector_results),
                    'successful': 0,
                    'success_rate': 0,
                    'avg_r2': 0,
                    'max_r2': 0,
                    'min_r2': 0,
                    'avg_mse': 0,
                    'avg_training_time': 0,
                    'best_symbol': 'N/A'
                }
        
        # Phân tích tổng thể
        successful_results = [r for r in results if r['status'] == 'success']
        failed_results = [r for r in results if r['status'] == 'failed']
        
        if successful_results:
            overall_r2 = [r.get('r2', 0) for r in successful_results]
            overall_mse = [r.get('mse', 0) for r in successful_results]
            overall_times = [r.get('training_time', 0) for r in successful_results]
            
            # Top performers
            top_performers = sorted(successful_results, key=lambda x: x.get('r2', 0), reverse=True)[:10]
            worst_performers = sorted(successful_results, key=lambda x: x.get('r2', 0))[:10]
            
            summary = {
                'overall': {
                    'total_symbols': len(results),
                    'successful': len(successful_results),
                    'failed': len(failed_results),
                    'success_rate': len(successful_results) / len(results),
                    'avg_r2': np.mean(overall_r2),
                    'max_r2': np.max(overall_r2),
                    'min_r2': np.min(overall_r2),
                    'avg_mse': np.mean(overall_mse),
                    'avg_training_time': np.mean(overall_times),
                    'total_training_time': np.sum(overall_times)
                },
                'sector_analysis': sector_analysis,
                'top_performers': [
                    {
                        'symbol': r['symbol'],
                        'sector': r['sector'],
                        'r2': r.get('r2', 0),
                        'mse': r.get('mse', 0),
                        'training_time': r.get('training_time', 0)
                    }
                    for r in top_performers
                ],
                'worst_performers': [
                    {
                        'symbol': r['symbol'],
                        'sector': r['sector'],
                        'r2': r.get('r2', 0),
                        'mse': r.get('mse', 0),
                        'training_time': r.get('training_time', 0)
                    }
                    for r in worst_performers
                ],
                'failed_symbols': [
                    {
                        'symbol': r['symbol'],
                        'sector': r['sector'],
                        'error': r.get('error', 'Unknown error')
                    }
                    for r in failed_results
                ]
            }
        else:
            summary = {
                'overall': {
                    'total_symbols': len(results),
                    'successful': 0,
                    'failed': len(failed_results),
                    'success_rate': 0,
                    'avg_r2': 0,
                    'max_r2': 0,
                    'min_r2': 0,
                    'avg_mse': 0,
                    'avg_training_time': 0,
                    'total_training_time': 0
                },
                'sector_analysis': sector_analysis,
                'top_performers': [],
                'worst_performers': [],
                'failed_symbols': [
                    {
                        'symbol': r['symbol'],
                        'sector': r['sector'],
                        'error': r.get('error', 'Unknown error')
                    }
                    for r in failed_results
                ]
            }
        
        return summary
    
    def save_results(self, results: List[Dict], summary: Dict[str, Any]):
        """Lưu kết quả training"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Lưu kết quả chi tiết
        detailed_file = f"results/training_results_{timestamp}.json"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        # Lưu báo cáo tổng hợp
        summary_file = f"results/training_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        # Tạo báo cáo CSV
        csv_file = f"results/training_results_{timestamp}.csv"
        self.create_csv_report(results, csv_file)
        
        self.logger.info(f"Results saved to: {detailed_file}, {summary_file}, {csv_file}")
    
    def create_csv_report(self, results: List[Dict], file_path: str):
        """Tạo báo cáo CSV"""
        df_data = []
        for result in results:
            row = {
                'Symbol': result['symbol'],
                'Sector': result['sector'],
                'Status': result['status'],
                'R2_Score': result.get('r2', 'N/A'),
                'MSE': result.get('mse', 'N/A'),
                'MAE': result.get('mae', 'N/A'),
                'Training_Time': result.get('training_time', 'N/A'),
                'Data_Points': result.get('data_points', 'N/A'),
                'Error': result.get('error', 'N/A')
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df.to_csv(file_path, index=False, encoding='utf-8')

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/batch_training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )
    
    # Train tất cả các mã cổ phiếu
    trainer = BatchTrainer()
    results = trainer.train_all_stocks()
    
    print("Training completed!")
    print(f"Total symbols: {results['total_symbols']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {results['successful']/results['total_symbols']:.2%}")
    
    if 'summary' in results:
        summary = results['summary']
        print(f"Average R²: {summary['overall']['avg_r2']:.4f}")
        print(f"Best R²: {summary['overall']['max_r2']:.4f}")
        print(f"Total training time: {summary['overall']['total_training_time']:.2f}s")
