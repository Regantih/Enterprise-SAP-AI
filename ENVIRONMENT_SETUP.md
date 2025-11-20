# 🚀 Development Environment Setup Guide

Complete guide for seamless integration of **GitHub**, **Kaggle**, and **VS Code** for your Tunix Hackathon project.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub Setup](#github-setup)
3. [Kaggle API Configuration](#kaggle-api-configuration)
4. [VS Code Configuration](#vs-code-configuration)
5. [Workflow Automation](#workflow-automation)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Your current environment:
- ✅ **Git**: 2.52.0.windows.1
- ✅ **Python**: 3.14.0
- ✅ **VS Code**: Installed
- ✅ **Git User**: Regantih (regantih@gmail.com)

---

## 🐙 GitHub Setup

### Step 1: Initialize Git Repository

```powershell
# Navigate to your project directory
cd "c:\Users\hrega\OneDrive\Documents\Antigravity"

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Tunix Hackathon project"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click **"New Repository"** (+ icon in top right)
3. Name it: `tunix-hackathon` or your preferred name
4. Choose **Private** or **Public**
5. **Do NOT** initialize with README (we already have files)
6. Click **"Create repository"**

### Step 3: Connect Local Repository to GitHub

```powershell
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tunix-hackathon.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Configure Git Credentials (Optional)

For easier authentication, use GitHub CLI or Personal Access Token:

```powershell
# Install GitHub CLI (if not installed)
winget install GitHub.cli

# Authenticate with GitHub
gh auth login
```

---

## 🏆 Kaggle API Configuration

### Step 1: Get Kaggle API Credentials

1. Go to [Kaggle](https://www.kaggle.com)
2. Click on your profile picture → **Settings**
3. Scroll to **API** section
4. Click **"Create New Token"**
5. This downloads `kaggle.json` file

### Step 2: Install Kaggle API

```powershell
# Install Kaggle package
python -m pip install kaggle
```

### Step 3: Configure Kaggle Credentials

```powershell
# Create .kaggle directory in your user folder
mkdir $env:USERPROFILE\.kaggle -Force

# Move kaggle.json to the .kaggle directory
# (Download kaggle.json from Kaggle first, then run:)
Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$env:USERPROFILE\.kaggle\kaggle.json" -Force
```

### Step 4: Test Kaggle API

```powershell
# List your Kaggle notebooks
kaggle kernels list --mine

# Download a specific notebook
kaggle kernels pull hemanthreganti/winner-trajectory-reward-grpo-training
```

---

## 💻 VS Code Configuration

### Essential Extensions

Install these extensions for optimal Python/Jupyter development:

1. **Python** (Microsoft) - `ms-python.python`
2. **Jupyter** (Microsoft) - `ms-toolsai.jupyter`
3. **GitLens** (GitKraken) - `eamodio.gitlens`
4. **GitHub Pull Requests** (GitHub) - `github.pullrequest`
5. **Kaggle** (Kaggle) - `kaggle.kaggle` (if available)
6. **Python Indent** - `kevinrose.vsc-python-indent`
7. **autoDocstring** - `njpwerner.autodocstring`

#### Install via Command Line:

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension github.pullrequest
code --install-extension kevinrose.vsc-python-indent
code --install-extension njpwerner.autodocstring
```

### VS Code Settings

Create/update `.vscode/settings.json` in your project:

```json
{
  "python.defaultInterpreterPath": "python",
  "jupyter.askForKernelRestart": false,
  "jupyter.interactiveWindow.textEditor.executeSelection": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "git.autofetch": true,
  "git.confirmSync": false,
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.tabSize": 4
  },
  "[json]": {
    "editor.defaultFormatter": "vscode.json-language-features"
  }
}
```

### Recommended Keyboard Shortcuts

- **Run Cell**: `Ctrl+Enter`
- **Run Cell and Move Next**: `Shift+Enter`
- **Git Commit**: `Ctrl+Shift+G`
- **Command Palette**: `Ctrl+Shift+P`

---

## 🔄 Workflow Automation

### Create Helper Scripts

#### 1. Kaggle Sync Script (`sync_kaggle.py`)

```python
#!/usr/bin/env python3
"""
Sync notebooks between local and Kaggle
"""
import subprocess
import sys

def download_notebook(notebook_name):
    """Download notebook from Kaggle"""
    cmd = f"kaggle kernels pull {notebook_name}"
    subprocess.run(cmd, shell=True, check=True)
    print(f"✅ Downloaded: {notebook_name}")

def push_notebook(notebook_path):
    """Push notebook to Kaggle"""
    cmd = f"kaggle kernels push -p {notebook_path}"
    subprocess.run(cmd, shell=True, check=True)
    print(f"✅ Pushed: {notebook_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync_kaggle.py [download|push] [notebook_name/path]")
        sys.exit(1)
    
    action = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else None
    
    if action == "download" and target:
        download_notebook(target)
    elif action == "push" and target:
        push_notebook(target)
    else:
        print("Invalid action or missing target")
```

#### 2. Git Workflow Script (`git_workflow.ps1`)

```powershell
# Quick Git workflow
param(
    [string]$message = "Update notebook"
)

Write-Host "🔄 Starting Git workflow..." -ForegroundColor Cyan

# Add all changes
git add .
Write-Host "✅ Staged changes" -ForegroundColor Green

# Commit
git commit -m $message
Write-Host "✅ Committed: $message" -ForegroundColor Green

# Push
git push
Write-Host "✅ Pushed to GitHub" -ForegroundColor Green

Write-Host "🎉 Done!" -ForegroundColor Cyan
```

**Usage:**
```powershell
.\git_workflow.ps1 -message "Fixed trajectory reward implementation"
```

### Create .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# Kaggle
kaggle.json
.kaggle/

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# Environment
.env
.venv

# OS
.DS_Store
Thumbs.db

# Large files
*.msix
*.zip
*.tar.gz
```

---

## 🔧 Complete Workflow Example

### Daily Development Workflow

```powershell
# 1. Start your day - pull latest from GitHub
git pull origin main

# 2. Download latest notebook from Kaggle
kaggle kernels pull hemanthreganti/winner-trajectory-reward-grpo-training

# 3. Open in VS Code
code "winner-trajectory-reward-grpo-training.ipynb"

# 4. Make changes in VS Code...

# 5. Test locally (if possible)
python -m jupyter nbconvert --to notebook --execute your_notebook.ipynb

# 6. Commit to Git
git add .
git commit -m "Improved GRPO training implementation"
git push

# 7. Push to Kaggle (create kernel-metadata.json first - see below)
kaggle kernels push -p .
```

### Kaggle Notebook Metadata

Create `kernel-metadata.json` for pushing notebooks to Kaggle:

```json
{
  "id": "hemanthreganti/winner-trajectory-reward-grpo-training",
  "title": "🏆 WINNER - Trajectory Reward GRPO Training",
  "code_file": "winner-trajectory-reward-grpo-training.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": false,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": [],
  "competition_sources": [],
  "kernel_sources": []
}
```

---

## 🐛 Troubleshooting

### Issue: Git Push Requires Password Every Time

**Solution**: Use GitHub CLI or configure credential helper

```powershell
# Option 1: GitHub CLI (recommended)
gh auth login

# Option 2: Git Credential Manager
git config --global credential.helper wincred
```

### Issue: Kaggle API Not Found

**Solution**: Ensure Kaggle is installed and in PATH

```powershell
python -m pip install --upgrade kaggle
```

### Issue: VS Code Can't Find Python

**Solution**: Set Python interpreter

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose Python 3.14.0

### Issue: Jupyter Kernel Not Starting

**Solution**: Install ipykernel

```powershell
python -m pip install ipykernel
python -m ipykernel install --user
```

---

## 🎯 Quick Reference Commands

| Task | Command |
|------|---------|
| **Git Status** | `git status` |
| **Git Commit** | `git add . && git commit -m "message"` |
| **Git Push** | `git push` |
| **Git Pull** | `git pull` |
| **List Kaggle Notebooks** | `kaggle kernels list --mine` |
| **Download Kaggle Notebook** | `kaggle kernels pull USERNAME/NOTEBOOK` |
| **Push to Kaggle** | `kaggle kernels push -p .` |
| **Open in VS Code** | `code .` |
| **Install Package** | `python -m pip install PACKAGE` |

---

## 📚 Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

## 🎉 You're All Set!

Your development environment is now configured for seamless workflow between:
- 💻 **Local development** in VS Code
- 🐙 **Version control** with GitHub
- 🏆 **Notebook execution** on Kaggle

Happy coding and good luck with the Tunix Hackathon! 🚀
