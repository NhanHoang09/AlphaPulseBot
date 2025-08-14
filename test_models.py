#!/usr/bin/env python3
"""
LSTM Training Test Wrapper
Script wrapper để test training functionality từ root level
"""

import sys
import os
import subprocess

def main():
    """Main function"""
    # Chuyển đến thư mục training và chạy test
    training_dir = os.path.join(os.path.dirname(__file__), 'src', 'ml', 'training')
    
    print("=" * 60)
    print("LSTM TRAINING TEST")
    print("=" * 60)
    print()
    
    # Chạy test script
    cmd = [sys.executable, 'test_training.py']
    result = subprocess.run(cmd, cwd=training_dir)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("You can now use:")
        print("  python train_models.py status")
        print("  python train_models.py train-single AAPL TECHNOLOGY")
    else:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED!")
        print("=" * 60)
        print()
        print("Please check the logs and fix issues.")

if __name__ == "__main__":
    main()
