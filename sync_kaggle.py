#!/usr/bin/env python3
"""
Sync notebooks between local and Kaggle

Usage:
    python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training
    python sync_kaggle.py push .
"""
import subprocess
import sys
import os

def download_notebook(notebook_name):
    """Download notebook from Kaggle"""
    print(f"📥 Downloading notebook: {notebook_name}")
    cmd = f"kaggle kernels pull {notebook_name}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Downloaded: {notebook_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading notebook: {e}")
        sys.exit(1)

def push_notebook(notebook_path):
    """Push notebook to Kaggle"""
    print(f"📤 Pushing notebook from: {notebook_path}")
    
    # Check if kernel-metadata.json exists
    metadata_path = os.path.join(notebook_path, "kernel-metadata.json")
    if not os.path.exists(metadata_path):
        print(f"⚠️  Warning: kernel-metadata.json not found in {notebook_path}")
        print("Creating a template kernel-metadata.json file...")
        create_metadata_template(notebook_path)
    
    cmd = f"kaggle kernels push -p {notebook_path}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Pushed: {notebook_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing notebook: {e}")
        sys.exit(1)

def create_metadata_template(notebook_path):
    """Create a template kernel-metadata.json file"""
    template = """{
  "id": "YOUR_USERNAME/YOUR_NOTEBOOK_NAME",
  "title": "Your Notebook Title",
  "code_file": "notebook.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": false,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": [],
  "competition_sources": [],
  "kernel_sources": []
}"""
    
    metadata_path = os.path.join(notebook_path, "kernel-metadata.json")
    with open(metadata_path, 'w') as f:
        f.write(template)
    print(f"✅ Created template: {metadata_path}")
    print("⚠️  Please edit kernel-metadata.json with your notebook details before pushing!")

def list_notebooks():
    """List user's Kaggle notebooks"""
    print("📋 Listing your Kaggle notebooks...")
    cmd = "kaggle kernels list --mine"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error listing notebooks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sync_kaggle.py download <notebook_name>")
        print("  python sync_kaggle.py push <path>")
        print("  python sync_kaggle.py list")
        print("\nExamples:")
        print("  python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training")
        print("  python sync_kaggle.py push .")
        print("  python sync_kaggle.py list")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "download":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide notebook name")
            print("Example: python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training")
            sys.exit(1)
        download_notebook(sys.argv[2])
    elif action == "push":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        push_notebook(target)
    elif action == "list":
        list_notebooks()
    else:
        print(f"❌ Unknown action: {action}")
        print("Valid actions: download, push, list")
        sys.exit(1)
