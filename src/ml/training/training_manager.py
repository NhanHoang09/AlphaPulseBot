"""
Training Manager
Quản lý tất cả các chức năng training LSTM models
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from .batch_trainer import BatchTrainer

class TrainingManager:
    """Manager để quản lý tất cả các hoạt động training"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.batch_trainer = BatchTrainer()
        
        # Tạo các thư mục cần thiết
        self._create_directories()
    
    def _create_directories(self):
        """Tạo các thư mục cần thiết"""
        directories = [
            "models",
            "results", 
            "logs",
            "results/plots"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_training_status(self) -> Dict[str, Any]:
        """Lấy trạng thái training hiện tại"""
        try:
            # Kiểm tra số lượng models đã được train
            models_dir = "models"
            if not os.path.exists(models_dir):
                return {
                    'status': 'no_models',
                    'total_models': 0,
                    'message': 'Chưa có models nào được train'
                }
            
            # Đếm số lượng models LSTM
            lstm_models = [f for f in os.listdir(models_dir) if f.startswith('lstm_') and f.endswith('.h5')]
            
            # Đếm số lượng scalers
            scalers = [f for f in os.listdir(models_dir) if f.startswith('lstm_scaler_') and f.endswith('.pkl')]
            target_scalers = [f for f in os.listdir(models_dir) if f.startswith('lstm_target_scaler_') and f.endswith('.pkl')]
            
            # Lấy danh sách symbols đã được train
            symbols = []
            for model_file in lstm_models:
                symbol = model_file.replace('lstm_', '').replace('.h5', '')
                symbols.append(symbol)
            
            return {
                'status': 'has_models',
                'total_models': len(lstm_models),
                'total_scalers': len(scalers),
                'total_target_scalers': len(target_scalers),
                'trained_symbols': symbols,
                'message': f'Đã có {len(lstm_models)} models được train'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting training status: {str(e)}")
            return {
                'status': 'error',
                'message': f'Lỗi khi kiểm tra trạng thái: {str(e)}'
            }
    
    def get_latest_training_results(self) -> Optional[Dict[str, Any]]:
        """Lấy kết quả training mới nhất"""
        try:
            results_dir = "results"
            if not os.path.exists(results_dir):
                return None
            
            # Tìm file summary mới nhất
            import glob
            summary_files = glob.glob(os.path.join(results_dir, "training_summary_*.json"))
            if not summary_files:
                return None
            
            latest_summary = max(summary_files, key=os.path.getctime)
            
            # Load summary
            import json
            with open(latest_summary, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            
            return {
                'summary': summary,
                'file_path': latest_summary,
                'timestamp': os.path.basename(latest_summary).replace('training_summary_', '').replace('.json', '')
            }
            
        except Exception as e:
            self.logger.error(f"Error getting latest results: {str(e)}")
            return None
    
    def train_single_stock(self, symbol: str, sector: str = "UNKNOWN") -> Dict[str, Any]:
        """Train model cho một mã cổ phiếu"""
        try:
            self.logger.info(f"Training single stock: {symbol} ({sector})")
            
            # Khởi tạo detailed report cho single stock
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.batch_trainer.detailed_report_generator.start_report(timestamp)
            
            result = self.batch_trainer.train_single_stock(symbol, sector)
            
            # Thêm kết quả vào detailed report
            self.batch_trainer.detailed_report_generator.add_stock_result(result)
            
            # Tạo summary cho single stock
            summary = {
                'total_symbols': 1,
                'successful': 1 if result['status'] == 'success' else 0,
                'failed': 0 if result['status'] == 'success' else 1,
                'success_rate': 1.0 if result['status'] == 'success' else 0.0,
                'avg_r2': result.get('r2', 0) if result['status'] == 'success' else 0,
                'max_r2': result.get('r2', 0) if result['status'] == 'success' else 0,
                'min_r2': result.get('r2', 0) if result['status'] == 'success' else 0,
                'avg_training_time': result.get('training_time', 0),
                'top_performers': [result] if result['status'] == 'success' else [],
                'sector_analysis': {
                    sector: {
                        'total_symbols': 1,
                        'successful': 1 if result['status'] == 'success' else 0,
                        'success_rate': 1.0 if result['status'] == 'success' else 0.0,
                        'avg_r2': result.get('r2', 0) if result['status'] == 'success' else 0,
                        'best_symbol': symbol if result['status'] == 'success' else 'N/A'
                    }
                }
            }
            
            # Thêm summary vào detailed report
            self.batch_trainer.detailed_report_generator.add_summary(summary)
            
            # Cập nhật trạng thái
            status = self.get_training_status()
            
            return {
                'training_result': result,
                'current_status': status,
                'detailed_report_path': self.batch_trainer.detailed_report_generator.get_report_path()
            }
            
        except Exception as e:
            self.logger.error(f"Error training single stock {symbol}: {str(e)}")
            return {
                'training_result': {
                    'symbol': symbol,
                    'sector': sector,
                    'status': 'failed',
                    'error': str(e)
                },
                'current_status': self.get_training_status()
            }
    
    def train_multiple_stocks(self, symbols: List[tuple]) -> Dict[str, Any]:
        """Train models cho nhiều mã cổ phiếu"""
        try:
            self.logger.info(f"Training multiple stocks: {len(symbols)} symbols")
            
            # Khởi tạo detailed report cho multiple stocks
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.batch_trainer.detailed_report_generator.start_report(timestamp)
            
            # Tạo sectors dict cho batch trainer
            sectors = {}
            for symbol, sector in symbols:
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append(symbol)
            
            # Train từng mã
            results = []
            successful_count = 0
            failed_count = 0
            
            for i, (symbol, sector) in enumerate(symbols, 1):
                self.logger.info(f"Progress: {i}/{len(symbols)} - Training {symbol}")
                
                result = self.batch_trainer.train_single_stock(symbol, sector)
                results.append(result)
                
                # Thêm kết quả vào detailed report
                self.batch_trainer.detailed_report_generator.add_stock_result(result)
                
                if result['status'] == 'success':
                    successful_count += 1
                else:
                    failed_count += 1
            
            # Tạo báo cáo tổng hợp
            summary = self.batch_trainer.create_training_summary(results, sectors)
            
            # Thêm summary vào detailed report
            self.batch_trainer.detailed_report_generator.add_summary(summary)
            
            # Lưu kết quả
            self.batch_trainer.save_results(results, summary)
            
            return {
                'results': results,
                'summary': summary,
                'total_symbols': len(symbols),
                'successful': successful_count,
                'failed': failed_count,
                'success_rate': successful_count / len(symbols) if symbols else 0,
                'detailed_report_path': self.batch_trainer.detailed_report_generator.get_report_path()
            }
            
        except Exception as e:
            self.logger.error(f"Error training multiple stocks: {str(e)}")
            return {
                'error': str(e),
                'results': [],
                'summary': None
            }
    
    def train_all_stocks_from_file(self, file_path: str = "data/top_10_data.md") -> Dict[str, Any]:
        """Train tất cả các mã cổ phiếu từ file"""
        try:
            self.logger.info(f"Training all stocks from file: {file_path}")
            result = self.batch_trainer.train_all_stocks(file_path)
            
            # Hiển thị thông tin về detailed report
            if 'detailed_report_path' in result and result['detailed_report_path']:
                print(f"\n📄 Detailed Report: {result['detailed_report_path']}")
                print("   Báo cáo chi tiết cho từng mã cổ phiếu đã được tạo!")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error training all stocks: {str(e)}")
            return {
                'error': str(e)
            }
    
    def get_model_info(self, symbol: str) -> Dict[str, Any]:
        """Lấy thông tin model của một mã cổ phiếu"""
        try:
            model_path = f"models/lstm_{symbol}.h5"
            scaler_path = f"models/lstm_scaler_{symbol}.pkl"
            target_scaler_path = f"models/lstm_target_scaler_{symbol}.pkl"
            
            info = {
                'symbol': symbol,
                'model_exists': os.path.exists(model_path),
                'scaler_exists': os.path.exists(scaler_path),
                'target_scaler_exists': os.path.exists(target_scaler_path),
                'model_path': model_path if os.path.exists(model_path) else None,
                'scaler_path': scaler_path if os.path.exists(scaler_path) else None,
                'target_scaler_path': target_scaler_path if os.path.exists(target_scaler_path) else None
            }
            
            # Lấy thông tin file
            if info['model_exists']:
                import stat
                stat_info = os.stat(model_path)
                info['model_size'] = stat_info.st_size
                info['created_time'] = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                info['modified_time'] = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting model info for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def delete_model(self, symbol: str) -> Dict[str, Any]:
        """Xóa model của một mã cổ phiếu"""
        try:
            files_to_delete = [
                f"models/lstm_{symbol}.h5",
                f"models/lstm_scaler_{symbol}.pkl",
                f"models/lstm_target_scaler_{symbol}.pkl"
            ]
            
            deleted_files = []
            for file_path in files_to_delete:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
            
            return {
                'symbol': symbol,
                'deleted_files': deleted_files,
                'message': f'Đã xóa {len(deleted_files)} files cho {symbol}'
            }
            
        except Exception as e:
            self.logger.error(f"Error deleting model for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e)
            }
    
    def cleanup_old_results(self, days: int = 30) -> Dict[str, Any]:
        """Dọn dẹp các kết quả cũ"""
        try:
            import glob
            from datetime import timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            cleaned_files = []
            
            # Dọn dẹp results
            results_dir = "results"
            if os.path.exists(results_dir):
                for file_path in glob.glob(os.path.join(results_dir, "*")):
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                        if file_time < cutoff_date:
                            os.remove(file_path)
                            cleaned_files.append(file_path)
            
            # Dọn dẹp logs
            logs_dir = "logs"
            if os.path.exists(logs_dir):
                for file_path in glob.glob(os.path.join(logs_dir, "*")):
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                        if file_time < cutoff_date:
                            os.remove(file_path)
                            cleaned_files.append(file_path)
            
            return {
                'cleaned_files': cleaned_files,
                'total_cleaned': len(cleaned_files),
                'cutoff_date': cutoff_date.strftime('%Y-%m-%d'),
                'message': f'Đã dọn dẹp {len(cleaned_files)} files cũ hơn {days} ngày'
            }
            
        except Exception as e:
            self.logger.error(f"Error cleaning old results: {str(e)}")
            return {
                'error': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test training manager
    manager = TrainingManager()
    
    # Get status
    status = manager.get_training_status()
    print("Training Status:", status)
    
    # Get latest results
    latest = manager.get_latest_training_results()
    if latest:
        print("Latest Results:", latest['timestamp'])
    
    # Train a single stock
    result = manager.train_single_stock("AAPL", "TECHNOLOGY")
    print("Single Stock Result:", result['training_result']['status'])
