"""
Fetch Kaggle kernel logs for the given kernel slug.
"""
from kaggle import api
import json
import os

KERNEL_SLUG = "hemanthreganti/winner-trajectory-reward-grpo-training-gemm"
OUTPUT_DIR = "kaggle_logs"

def fetch_logs():
    try:
        api.authenticate()
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        # This will download the notebook output (including logs) as a zip
        api.kernels_output(KERNEL_SLUG, path=OUTPUT_DIR, force=True)
        print(f"✅ Logs downloaded to {OUTPUT_DIR}")
    except Exception as e:
        print(f"❌ Failed to fetch logs: {e}")

if __name__ == "__main__":
    fetch_logs()
