# Training Module

Module này chứa tất cả các chức năng liên quan đến training LSTM models cho cổ phiếu.

## Cấu trúc

```
src/ml/training/
├── __init__.py              # Module initialization
├── batch_trainer.py         # Batch training functionality
├── training_manager.py      # Training management
├── cli.py                   # Command line interface
└── README.md               # This file
```

## Components

### 1. BatchTrainer (`batch_trainer.py`)

Class chính để thực hiện batch training cho nhiều mã cổ phiếu.

**Tính năng:**

- Trích xuất danh sách mã cổ phiếu từ file markdown
- Train model cho từng mã cổ phiếu
- Tạo báo cáo tổng hợp
- Lưu kết quả dưới dạng JSON, CSV

**Methods:**

- `extract_stock_symbols()` - Trích xuất danh sách mã
- `train_single_stock()` - Train một mã cổ phiếu
- `train_all_stocks()` - Train tất cả mã cổ phiếu
- `create_training_summary()` - Tạo báo cáo tổng hợp
- `save_results()` - Lưu kết quả

### 2. TrainingManager (`training_manager.py`)

Manager để quản lý tất cả các hoạt động training.

**Tính năng:**

- Quản lý trạng thái training
- Train single/multiple stocks
- Quản lý models (info, delete)
- Dọn dẹp files cũ

**Methods:**

- `get_training_status()` - Lấy trạng thái hiện tại
- `get_latest_training_results()` - Lấy kết quả mới nhất
- `train_single_stock()` - Train một mã
- `train_multiple_stocks()` - Train nhiều mã
- `train_all_stocks_from_file()` - Train từ file
- `get_model_info()` - Thông tin model
- `delete_model()` - Xóa model
- `cleanup_old_results()` - Dọn dẹp files cũ

### 3. CLI Tool (`cli.py`)

Command line interface để quản lý training.

**Commands:**

- `status` - Hiển thị trạng thái
- `train-single` - Train một mã cổ phiếu
- `train-multiple` - Train nhiều mã cổ phiếu
- `train-all` - Train tất cả từ file
- `info` - Thông tin model
- `delete` - Xóa model
- `cleanup` - Dọn dẹp files cũ

## Usage

### Python API

```python
from src.ml.training import BatchTrainer, TrainingManager

# Sử dụng BatchTrainer
trainer = BatchTrainer()
result = trainer.train_single_stock("AAPL", "TECHNOLOGY")

# Sử dụng TrainingManager
manager = TrainingManager()
status = manager.get_training_status()
result = manager.train_single_stock("AAPL", "TECHNOLOGY")
```

### Command Line

```bash
# Hiển thị trạng thái
python src/ml/training/cli.py status

# Train một mã cổ phiếu
python src/ml/training/cli.py train-single AAPL TECHNOLOGY

# Train nhiều mã cổ phiếu
python src/ml/training/cli.py train-multiple AAPL:TECHNOLOGY MSFT:TECHNOLOGY

# Train tất cả từ file
python src/ml/training/cli.py train-all data/top_10_data.md

# Xem thông tin model
python src/ml/training/cli.py info AAPL

# Xóa model
python src/ml/training/cli.py delete AAPL

# Dọn dẹp files cũ
python src/ml/training/cli.py cleanup 30
```

## Output Files

### Models

```
models/
├── lstm_SYMBOL.h5                    # LSTM model
├── lstm_scaler_SYMBOL.pkl           # Feature scaler
└── lstm_target_scaler_SYMBOL.pkl    # Target scaler
```

### Results

```
results/
├── training_results_TIMESTAMP.json   # Kết quả chi tiết
├── training_summary_TIMESTAMP.json   # Báo cáo tổng hợp
├── training_results_TIMESTAMP.csv    # Bảng dữ liệu
└── plots/
    └── training_analysis.png         # Biểu đồ phân tích
```

### Logs

```
logs/
├── batch_training_TIMESTAMP.log      # Log training toàn bộ
├── test_training_TIMESTAMP.log       # Log test training
└── international_test_TIMESTAMP.log  # Log test quốc tế
```

## Configuration

### Training Parameters

Các parameters có thể điều chỉnh trong `batch_trainer.py`:

```python
# Training parameters
epochs = 50              # Số epochs training
batch_size = 16          # Batch size
lookback = 30            # Số ngày nhìn lại
prediction_horizon = 1   # Số ngày dự báo trước
```

### Adaptive Parameters

Hệ thống tự động điều chỉnh parameters dựa trên đặc điểm cổ phiếu:

- **Conservative stocks**: epochs=80, batch_size=32, lookback=40
- **Aggressive stocks**: epochs=150, batch_size=8, lookback=25
- **Balanced stocks**: epochs=100, batch_size=16, lookback=30

## Error Handling

Module có error handling toàn diện:

1. **Data availability errors** - Xử lý khi không có dữ liệu
2. **Training errors** - Xử lý lỗi trong quá trình training
3. **File I/O errors** - Xử lý lỗi đọc/ghi file
4. **Model errors** - Xử lý lỗi model building

## Performance Metrics

Hệ thống đánh giá hiệu suất bằng:

- **R² Score** (0-1, càng cao càng tốt)
- **MSE** (Mean Squared Error)
- **MAE** (Mean Absolute Error)
- **Training Time**
- **Success Rate**

## Dependencies

```python
# Core dependencies
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Additional dependencies
import joblib
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
```

## Examples

### Train Single Stock

```python
from src.ml.training import TrainingManager

manager = TrainingManager()
result = manager.train_single_stock("AAPL", "TECHNOLOGY")

if result['training_result']['status'] == 'success':
    print(f"R² Score: {result['training_result']['r2']:.4f}")
```

### Train Multiple Stocks

```python
from src.ml.training import TrainingManager

manager = TrainingManager()
symbols = [("AAPL", "TECHNOLOGY"), ("MSFT", "TECHNOLOGY"), ("GOOGL", "TECHNOLOGY")]
result = manager.train_multiple_stocks(symbols)

print(f"Success rate: {result['success_rate']:.2%}")
```

### Get Training Status

```python
from src.ml.training import TrainingManager

manager = TrainingManager()
status = manager.get_training_status()

if status['status'] == 'has_models':
    print(f"Total models: {status['total_models']}")
    print(f"Trained symbols: {status['trained_symbols']}")
```

## Troubleshooting

### Common Issues

1. **"No data available"**

   - Kiểm tra kết nối internet
   - Kiểm tra mã cổ phiếu có tồn tại không
   - Thử với mã cổ phiếu quốc tế

2. **"Failed to add indicators"**

   - Dữ liệu không đủ để tính technical indicators
   - Kiểm tra format dữ liệu

3. **"Model performance is poor"**
   - R² score quá thấp (< 0.1)
   - Có thể cần tăng epochs hoặc điều chỉnh parameters

### Debug Mode

Sử dụng verbose mode để debug:

```bash
python src/ml/training/cli.py train-single AAPL TECHNOLOGY -v
```

## Contributing

Khi thêm tính năng mới:

1. Cập nhật docstring cho tất cả methods
2. Thêm error handling
3. Cập nhật README.md
4. Test với CLI tool
5. Cập nhật `__init__.py` nếu cần
