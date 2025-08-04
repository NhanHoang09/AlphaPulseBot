#!/usr/bin/env python3
"""
Debug Ollama Subprocess
Test subprocess call to Ollama
"""

import subprocess
import sys

def test_ollama_subprocess():
    """Test Ollama subprocess call"""
    print("🔧 Debug Ollama Subprocess")
    print("=" * 40)
    
    # Test 1: Check if ollama is available
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
        print(f"✅ Ollama version: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Ollama not found: {e}")
        return
    
    # Test 2: Test simple ollama run
    try:
        cmd = ["ollama", "run", "gpt_assistant:latest", "RSI là gì?"]
        print(f"\n🔍 Testing command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)  # 2 minutes
        print(f"Return code: {result.returncode}")
        print(f"Stdout length: {len(result.stdout)}")
        print(f"Stderr length: {len(result.stderr)}")
        
        if result.returncode == 0:
            print(f"✅ Success! Answer: {result.stdout[:200]}...")
        else:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ollama_subprocess() 