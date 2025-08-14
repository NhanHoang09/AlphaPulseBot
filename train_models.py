#!/usr/bin/env python3
"""
LSTM Training Wrapper
Script wrapper để truy cập training functionality từ root level
"""

import sys
import os
import subprocess

def main():
    """Main function"""
    # Chuyển đến thư mục training và chạy CLI
    training_dir = os.path.join(os.path.dirname(__file__), 'src', 'ml', 'training')
    
    if len(sys.argv) > 1:
        # Có arguments, chạy CLI tool
        args = sys.argv[1:]
        
        # Nếu có train-all với đường dẫn tương đối, chuyển thành tuyệt đối
        if len(args) >= 2 and args[0] == 'train-all' and not os.path.isabs(args[1]):
            args[1] = os.path.abspath(args[1])
        
        cmd = [sys.executable, 'train.py'] + args
        subprocess.run(cmd, cwd=training_dir)
    else:
        # Không có arguments, hiển thị help
        print("LSTM Training Tool")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python train_models.py status                    # Hiển thị trạng thái")
        print("  python train_models.py train-single AAPL TECH    # Train một mã")
        print("  python train_models.py test                      # Chạy test")
        print()
        print("Examples:")
        print("  python train_models.py status")
        print("  python train_models.py train-single AAPL TECHNOLOGY")
        print("  python train_models.py train-multiple AAPL:TECH MSFT:TECH")
        print("  python train_models.py train-all data/top_10_data.md")
        print("  python train_models.py info AAPL")
        print("  python train_models.py delete AAPL")
        print("  python train_models.py cleanup 30")
        print()
        print("For more help:")
        print("  python train_models.py --help")

if __name__ == "__main__":
    main()
