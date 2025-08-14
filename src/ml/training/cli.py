#!/usr/bin/env python3
"""
CLI Tool để quản lý LSTM Training
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Thêm thư mục src vào path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.ml.training.training_manager import TrainingManager

def setup_logging(verbose: bool = False):
    """Setup logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def status_command(manager: TrainingManager):
    """Hiển thị trạng thái training"""
    print("=" * 60)
    print("LSTM TRAINING STATUS")
    print("=" * 60)
    
    status = manager.get_training_status()
    
    if status['status'] == 'no_models':
        print("❌ Chưa có models nào được train")
        print(f"Message: {status['message']}")
    elif status['status'] == 'has_models':
        print(f"✅ Đã có {status['total_models']} models được train")
        print(f"📊 Scaler files: {status['total_scalers']}")
        print(f"🎯 Target scaler files: {status['total_target_scalers']}")
        print()
        print("📋 Danh sách mã đã train:")
        for symbol in status['trained_symbols']:
            print(f"  - {symbol}")
    else:
        print(f"❌ Lỗi: {status['message']}")
    
    # Hiển thị kết quả mới nhất
    latest = manager.get_latest_training_results()
    if latest:
        print(f"\n📈 Kết quả training mới nhất: {latest['timestamp']}")
        summary = latest['summary']
        if 'overall' in summary:
            overall = summary['overall']
            print(f"  Tổng số: {overall['total_symbols']}")
            print(f"  Thành công: {overall['successful']}")
            print(f"  Thất bại: {overall['failed']}")
            print(f"  Tỷ lệ thành công: {overall['success_rate']:.2%}")
            if overall['successful'] > 0:
                print(f"  R² trung bình: {overall['avg_r2']:.4f}")
                print(f"  R² tốt nhất: {overall['max_r2']:.4f}")

def train_single_command(manager: TrainingManager, symbol: str, sector: str):
    """Train model cho một mã cổ phiếu"""
    print(f"🚀 Training model cho {symbol} ({sector})...")
    
    result = manager.train_single_stock(symbol, sector)
    training_result = result['training_result']
    
    if training_result['status'] == 'success':
        print(f"✅ Training thành công!")
        print(f"  R² Score: {training_result.get('r2', 'N/A'):.4f}")
        print(f"  MSE: {training_result.get('mse', 'N/A'):.4f}")
        print(f"  Training Time: {training_result.get('training_time', 'N/A'):.2f}s")
    else:
        print(f"❌ Training thất bại!")
        print(f"  Error: {training_result.get('error', 'Unknown error')}")

def train_multiple_command(manager: TrainingManager, symbols: list):
    """Train models cho nhiều mã cổ phiếu"""
    print(f"🚀 Training models cho {len(symbols)} mã cổ phiếu...")
    
    # Parse symbols list
    symbol_list = []
    for symbol_str in symbols:
        if ':' in symbol_str:
            symbol, sector = symbol_str.split(':', 1)
            symbol_list.append((symbol.strip(), sector.strip()))
        else:
            symbol_list.append((symbol_str.strip(), "UNKNOWN"))
    
    result = manager.train_multiple_stocks(symbol_list)
    
    if 'error' in result:
        print(f"❌ Lỗi: {result['error']}")
        return
    
    print(f"✅ Training hoàn thành!")
    print(f"  Tổng số: {result['total_symbols']}")
    print(f"  Thành công: {result['successful']}")
    print(f"  Thất bại: {result['failed']}")
    print(f"  Tỷ lệ thành công: {result['success_rate']:.2%}")
    
    if result['summary'] and 'overall' in result['summary']:
        overall = result['summary']['overall']
        if overall['successful'] > 0:
            print(f"  R² trung bình: {overall['avg_r2']:.4f}")
            print(f"  R² tốt nhất: {overall['max_r2']:.4f}")

def train_all_command(manager: TrainingManager, file_path: str):
    """Train tất cả các mã cổ phiếu từ file"""
    print(f"🚀 Training tất cả các mã cổ phiếu từ {file_path}...")
    
    result = manager.train_all_stocks_from_file(file_path)
    
    if 'error' in result:
        print(f"❌ Lỗi: {result['error']}")
        return
    
    print(f"✅ Training hoàn thành!")
    print(f"  Tổng số: {result['total_symbols']}")
    print(f"  Thành công: {result['successful']}")
    print(f"  Thất bại: {result['failed']}")
    print(f"  Tỷ lệ thành công: {result['successful']/result['total_symbols']:.2%}")
    
    # Hiển thị thông tin về detailed report
    if 'detailed_report_path' in result and result['detailed_report_path']:
        print(f"\n📄 Detailed Report: {result['detailed_report_path']}")
        print("   Báo cáo chi tiết cho từng mã cổ phiếu đã được tạo!")
        print("   Bạn có thể mở file này để xem kết quả chi tiết của từng mã.")

def info_command(manager: TrainingManager, symbol: str):
    """Hiển thị thông tin model của một mã cổ phiếu"""
    print(f"📊 Thông tin model cho {symbol}:")
    
    info = manager.get_model_info(symbol)
    
    if 'error' in info:
        print(f"❌ Lỗi: {info['error']}")
        return
    
    print(f"  Model file: {'✅' if info['model_exists'] else '❌'}")
    print(f"  Scaler file: {'✅' if info['scaler_exists'] else '❌'}")
    print(f"  Target scaler file: {'✅' if info['target_scaler_exists'] else '❌'}")
    
    if info['model_exists']:
        print(f"  Model size: {info['model_size']} bytes")
        print(f"  Created: {info['created_time']}")
        print(f"  Modified: {info['modified_time']}")

def delete_command(manager: TrainingManager, symbol: str):
    """Xóa model của một mã cổ phiếu"""
    print(f"🗑️ Xóa model cho {symbol}...")
    
    result = manager.delete_model(symbol)
    
    if 'error' in result:
        print(f"❌ Lỗi: {result['error']}")
        return
    
    print(f"✅ {result['message']}")
    if result['deleted_files']:
        print("  Files đã xóa:")
        for file_path in result['deleted_files']:
            print(f"    - {file_path}")

def cleanup_command(manager: TrainingManager, days: int):
    """Dọn dẹp các kết quả cũ"""
    print(f"🧹 Dọn dẹp các files cũ hơn {days} ngày...")
    
    result = manager.cleanup_old_results(days)
    
    if 'error' in result:
        print(f"❌ Lỗi: {result['error']}")
        return
    
    print(f"✅ {result['message']}")
    print(f"  Cutoff date: {result['cutoff_date']}")
    print(f"  Files cleaned: {result['total_cleaned']}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="LSTM Training CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hiển thị trạng thái
  python cli.py status
  
  # Train một mã cổ phiếu
  python cli.py train-single AAPL TECHNOLOGY
  
  # Train nhiều mã cổ phiếu
  python cli.py train-multiple AAPL:TECHNOLOGY MSFT:TECHNOLOGY GOOGL:TECHNOLOGY
  
  # Train tất cả từ file
  python cli.py train-all data/top_10_data.md
  
  # Xem thông tin model
  python cli.py info AAPL
  
  # Xóa model
  python cli.py delete AAPL
  
  # Dọn dẹp files cũ
  python cli.py cleanup 30
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Hiển thị trạng thái training')
    
    # Train single command
    train_single_parser = subparsers.add_parser('train-single', help='Train model cho một mã cổ phiếu')
    train_single_parser.add_argument('symbol', help='Mã cổ phiếu')
    train_single_parser.add_argument('sector', help='Ngành')
    
    # Train multiple command
    train_multiple_parser = subparsers.add_parser('train-multiple', help='Train models cho nhiều mã cổ phiếu')
    train_multiple_parser.add_argument('symbols', nargs='+', help='Danh sách mã cổ phiếu (format: SYMBOL:SECTOR)')
    
    # Train all command
    train_all_parser = subparsers.add_parser('train-all', help='Train tất cả các mã cổ phiếu từ file')
    train_all_parser.add_argument('file', help='Đường dẫn file chứa danh sách mã cổ phiếu')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Hiển thị thông tin model')
    info_parser.add_argument('symbol', help='Mã cổ phiếu')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Xóa model')
    delete_parser.add_argument('symbol', help='Mã cổ phiếu')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Dọn dẹp files cũ')
    cleanup_parser.add_argument('days', type=int, help='Số ngày (files cũ hơn sẽ bị xóa)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Create manager
    manager = TrainingManager()
    
    # Execute command
    if args.command == 'status':
        status_command(manager)
    elif args.command == 'train-single':
        train_single_command(manager, args.symbol, args.sector)
    elif args.command == 'train-multiple':
        train_multiple_command(manager, args.symbols)
    elif args.command == 'train-all':
        train_all_command(manager, args.file)
    elif args.command == 'info':
        info_command(manager, args.symbol)
    elif args.command == 'delete':
        delete_command(manager, args.symbol)
    elif args.command == 'cleanup':
        cleanup_command(manager, args.days)

if __name__ == "__main__":
    main()
