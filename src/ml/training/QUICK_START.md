# Quick Start Guide - LSTM Training

## Cách sử dụng nhanh

### 1. Từ Root Level (Khuyến nghị)

```bash
# Hiển thị trạng thái training
python train_models.py status

# Train một mã cổ phiếu
python train_models.py train-single AAPL TECHNOLOGY

# Train nhiều mã cổ phiếu
python train_models.py train-multiple AAPL:TECHNOLOGY MSFT:TECHNOLOGY

# Train tất cả từ file
python train_models.py train-all data/top_10_data.md

# Test hệ thống
python test_models.py
```

### 2. Từ Training Directory

```bash
# Chuyển đến thư mục training
cd src/ml/training

# Hiển thị trạng thái
python train.py status

# Train một mã cổ phiếu
python train.py train-single AAPL TECHNOLOGY

# Test hệ thống
python test_training.py
```

### 3. Từ Python Code

```python
from src.ml.training import TrainingManager

# Khởi tạo manager
manager = TrainingManager()

# Lấy trạng thái
status = manager.get_training_status()
print(f"Total models: {status['total_models']}")

# Train một mã
result = manager.train_single_stock("AAPL", "TECHNOLOGY")
if result['training_result']['status'] == 'success':
    print(f"R²: {result['training_result']['r2']:.4f}")
```

## Các Commands Chính

### Status & Info

```bash
python train_models.py status          # Trạng thái training
python train_models.py info AAPL       # Thông tin model AAPL
```

### Training

```bash
python train_models.py train-single AAPL TECHNOLOGY
python train_models.py train-multiple AAPL:TECH MSFT:TECH
python train_models.py train-all data/top_10_data.md
```

### Management

```bash
python train_models.py delete AAPL     # Xóa model AAPL
python train_models.py cleanup 30      # Dọn dẹp files cũ hơn 30 ngày
```

### Help

```bash
python train_models.py --help          # Hiển thị help
python train_models.py train-single --help  # Help cho command cụ thể
```

## Cấu trúc Files

```
src/ml/training/
├── __init__.py              # Module initialization
├── batch_trainer.py         # Batch training functionality
├── training_manager.py      # Training management
├── cli.py                   # Command line interface
├── train.py                 # CLI wrapper
├── test_training.py         # Test script
├── README.md               # Documentation
├── TRAINING_REORGANIZATION.md  # Reorganization notes
└── QUICK_START.md          # This file
```

## Output Files

### Models

```
models/
├── lstm_AAPL.h5                    # LSTM model
├── lstm_scaler_AAPL.pkl           # Feature scaler
└── lstm_target_scaler_AAPL.pkl    # Target scaler
```

### Results

```
results/
├── training_results_TIMESTAMP.json   # Kết quả chi tiết
├── training_summary_TIMESTAMP.json   # Báo cáo tổng hợp
└── training_results_TIMESTAMP.csv    # Bảng dữ liệu
```

### Logs

```
logs/
├── batch_training_TIMESTAMP.log      # Log training toàn bộ
└── test_training_TIMESTAMP.log       # Log test training
```

## Troubleshooting

### Lỗi thường gặp

1. **"No data available"**

   - Kiểm tra kết nối internet
   - Thử với mã cổ phiếu quốc tế (AAPL, MSFT, GOOGL)

2. **"Module not found"**

   - Chạy từ root directory
   - Kiểm tra Python path

3. **"Permission denied"**
   - Chạy với quyền admin nếu cần
   - Kiểm tra quyền ghi vào thư mục

### Debug Mode

```bash
python train_models.py train-single AAPL TECHNOLOGY -v
```

## Examples

### Train và Test

```bash
# Test hệ thống
python test_models.py

# Train một mã cổ phiếu
python train_models.py train-single AAPL TECHNOLOGY

# Kiểm tra kết quả
python train_models.py status
python train_models.py info AAPL
```

### Batch Training

```bash
# Train nhiều mã cùng lúc
python train_models.py train-multiple AAPL:TECHNOLOGY MSFT:TECHNOLOGY GOOGL:TECHNOLOGY

# Train tất cả từ file
python train_models.py train-all data/top_10_data.md
```

### Management

```bash
# Xem thông tin model
python train_models.py info AAPL

# Xóa model nếu cần
python train_models.py delete AAPL

# Dọn dẹp files cũ
python train_models.py cleanup 30
```

## Performance Tips

1. **Sử dụng GPU** nếu có sẵn
2. **Tăng batch_size** nếu có đủ RAM
3. **Giảm epochs** để test nhanh
4. **Sử dụng verbose mode** để debug

## Support

- Xem `README.md` để biết thêm chi tiết
- Kiểm tra logs trong thư mục `logs/`
- Sử dụng `--help` để xem options
