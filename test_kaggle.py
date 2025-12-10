#!/usr/bin/env python3
"""Test Kaggle API"""
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

try:
    from kaggle import api
    print("✅ Kaggle import successful")
    
    api.authenticate()
    print("✅ Authentication successful")
    
    # Try to list notebooks
    kernels = api.kernels_list(mine=True)
    print(f"✅ Found {len(kernels)} notebooks")
    
    for kernel in kernels[:5]:  # Show first 5
        print(f"  - {kernel.title}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
