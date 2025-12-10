"""
Automated Kaggle Notebook Pusher - Uses Kaggle API directly
"""
import os
import json
import shutil
from pathlib import Path
from kaggle import api

# Configuration
NOTEBOOK_FILE = "winner_fixed_v6.ipynb"
KERNEL_SLUG = "hemanthreganti/winner-trajectory-reward-grpo-training-gemm"
TEMP_DIR = "kaggle_push_temp"

def create_kernel_metadata():
    """Create the kernel-metadata.json file required by Kaggle API."""
    metadata = {
        "id": KERNEL_SLUG,
        "title": "Winner Trajectory Reward GRPO Training Gemm",
        "code_file": NOTEBOOK_FILE,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": False,
        "enable_gpu": False,
        "enable_tpu": True,
        "enable_internet": True,
        "dataset_sources": ["thedevastator/grade-school-math-8k-q-a"],
        "competition_sources": [],
        "kernel_sources": ["google/gemma-2/Flax/gemma2-2b-it"]
    }
    return metadata

def push_to_kaggle():
    """Push the notebook to Kaggle using the API directly."""
    print("🚀 Preparing to push notebook to Kaggle...")
    
    # Authenticate
    try:
        api.authenticate()
        print("✅ Authenticated with Kaggle API")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Make sure you have ~/.kaggle/kaggle.json configured")
        print("   Download it from: https://www.kaggle.com/settings/account")
        return
    
    # Create temporary directory
    temp_path = Path(TEMP_DIR)
    if temp_path.exists():
        shutil.rmtree(temp_path)
    temp_path.mkdir()
    
    try:
        # Copy notebook to temp directory
        shutil.copy(NOTEBOOK_FILE, temp_path / NOTEBOOK_FILE)
        print(f"✅ Copied {NOTEBOOK_FILE} to temp directory")
        
        # Create metadata file
        metadata = create_kernel_metadata()
        with open(temp_path / "kernel-metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        print("✅ Created kernel-metadata.json")
        
        # Push to Kaggle
        print("\n📤 Pushing to Kaggle...")
        api.kernels_push(str(temp_path))
        
        print("\n✅ Successfully pushed to Kaggle!")
        print(f"   View at: https://www.kaggle.com/code/{KERNEL_SLUG}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path)
            print("\n🧹 Cleaned up temporary files")

if __name__ == "__main__":
    push_to_kaggle()
