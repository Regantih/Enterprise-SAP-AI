#!/usr/bin/env python3
"""
Sync notebooks between local and Kaggle

Usage:
    python kaggle_sync.py download hemanthreganti/winner-trajectory-reward-grpo-training
    python kaggle_sync.py push .
    python kaggle_sync.py list
"""
import sys
import os

# Import kaggle API
from kaggle import api

def download_notebook(notebook_name):
    """Download notebook from Kaggle"""
    print(f"📥 Downloading notebook: {notebook_name}")
    try:
        # Authenticate
        api.authenticate()
        
        # Parse username/kernel-slug
        parts = notebook_name.split('/')
        if len(parts) != 2:
            print("❌ Error: Notebook name should be in format: username/notebook-name")
            sys.exit(1)
        
        username, kernel_slug = parts
        api.kernels_pull(username, kernel_slug)
        print(f"✅ Downloaded: {notebook_name}")
    except Exception as e:
        print(f"❌ Error downloading notebook: {e}")
        print("\n💡 Make sure you have configured your Kaggle credentials:")
        print("   1. Download kaggle.json from https://www.kaggle.com/settings")
        print(f"   2. Place it in: {os.path.expanduser('~/.kaggle/kaggle.json')}")
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
        print("⚠️  Please edit kernel-metadata.json with your notebook details before pushing!")
        return
    
    try:
        # Authenticate
        api.authenticate()
        
        # Push kernel
        api.kernels_push(notebook_path)
        print(f"✅ Pushed: {notebook_path}")
    except Exception as e:
        print(f"❌ Error pushing notebook: {e}")
        print("\n💡 Make sure:")
        print("   1. kernel-metadata.json is properly configured")
        print("   2. You have Kaggle credentials set up")
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

def list_notebooks():
    """List user's Kaggle notebooks"""
    print("📋 Listing your Kaggle notebooks...")
    try:
        # Authenticate
        api.authenticate()
        
        # List kernels
        kernels = api.kernels_list(mine=True)
        
        if not kernels:
            print("No notebooks found.")
            return
        
        print("\n{:<50} {:<15} {:<10}".format("TITLE", "AUTHOR", "LANGUAGE"))
        print("-" * 75)
        for kernel in kernels:
            title = kernel.title[:47] + "..." if len(kernel.title) > 50 else kernel.title
            print("{:<50} {:<15} {:<10}".format(title, kernel.author, kernel.language))
        
        print(f"\nTotal: {len(kernels)} notebooks")
    except Exception as e:
        print(f"❌ Error listing notebooks: {e}")
        print("\n💡 Make sure you have configured your Kaggle credentials")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python kaggle_sync.py download <notebook_name>")
        print("  python kaggle_sync.py push <path>")
        print("  python kaggle_sync.py list")
        print("\nExamples:")
        print("  python kaggle_sync.py download hemanthreganti/winner-trajectory-reward-grpo-training")
        print("  python kaggle_sync.py push .")
        print("  python kaggle_sync.py list")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "download":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide notebook name")
            print("Example: python kaggle_sync.py download hemanthreganti/winner-trajectory-reward-grpo-training")
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
