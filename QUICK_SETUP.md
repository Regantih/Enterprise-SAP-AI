# Quick Setup Instructions

## ✅ Completed Steps

1. ✅ **Kaggle API Installed** - v1.7.4.5
2. ✅ **Git Repository Initialized** - Initial commit created
3. ✅ **VS Code Extensions Installed**:
   - Python v2025.6.1
   - Jupyter v2025.4.1
   - GitLens v17.7.1

## 🔄 Next: Configure Kaggle Credentials

### Step 1: Download Kaggle API Token

1. Open [Kaggle Settings](https://www.kaggle.com/settings) in your browser
2. Scroll to the **API** section
3. Click **"Create New Token"**
4. This will download `kaggle.json` to your Downloads folder

### Step 2: Move Kaggle Credentials

Run these commands in PowerShell:

```powershell
# Create .kaggle directory
mkdir $env:USERPROFILE\.kaggle -Force

# Move the downloaded kaggle.json
Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$env:USERPROFILE\.kaggle\kaggle.json" -Force
```

### Step 3: Test Kaggle Integration

```powershell
# Test Kaggle API
python -m kaggle kernels list --mine

# Or use the helper script
python sync_kaggle.py list
```

## 🐙 Next: Create GitHub Repository

### Option 1: Using GitHub Website

1. Go to [GitHub - New Repository](https://github.com/new)
2. Name: `tunix-hackathon` (or your choice)
3. Choose **Private** or **Public**
4. **Do NOT** initialize with README
5. Click **"Create repository"**

### Option 2: Using GitHub CLI (if installed)

```powershell
gh repo create tunix-hackathon --private --source=. --remote=origin --push
```

### Connect Local Repository to GitHub

After creating the repository on GitHub:

```powershell
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tunix-hackathon.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🎯 Quick Reference

### Kaggle Commands
```powershell
# List notebooks
python sync_kaggle.py list

# Download notebook
python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training

# Push notebook
python sync_kaggle.py push .
```

### Git Commands
```powershell
# Quick commit and push
.\git_workflow.ps1 -message "Your commit message"

# Manual workflow
git add .
git commit -m "Your message"
git push
```

## 📚 Full Documentation

See [ENVIRONMENT_SETUP.md](file:///c:/Users/hrega/OneDrive/Documents/Antigravity/ENVIRONMENT_SETUP.md) for complete details.
