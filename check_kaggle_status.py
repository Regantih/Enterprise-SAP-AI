"""
Check the status of Kaggle notebook versions
"""
from kaggle import api
import json

# Authenticate
api.authenticate()

# Get kernel status
kernel_slug = "hemanthreganti/winner-trajectory-reward-grpo-training-gemm"

try:
    # List kernel versions
    print("Fetching kernel versions...")
    versions = api.kernels_list(user="hemanthreganti", search=kernel_slug.split('/')[-1])
    
    for version in versions:
        print(f"\nKernel: {version.ref}")
        if hasattr(version, 'last_run_time'):
            print(f"  Last Run Time: {version.last_run_time}")
        print(f"  Total Votes: {version.total_votes}")
        
    # Get detailed kernel info
    print("\n" + "="*50)
    print("Getting detailed kernel status...")
    kernel_status = api.kernels_status(kernel_slug)
    
    print(f"\nStatus: {kernel_status}")
    print(f"Type: {type(kernel_status)}")
    
    if hasattr(kernel_status, '__dict__'):
        print("\nKernel Status Details:")
        for key, value in kernel_status.__dict__.items():
            print(f"  {key}: {value}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
