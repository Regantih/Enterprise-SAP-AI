# Tunix Hackathon Project

Machine learning project for the Google Tunix Hackathon featuring GRPO (Group Relative Policy Optimization) training with trajectory rewards.

## 📁 Project Structure

- `winner_fixed.ipynb` - Main notebook with GRPO training implementation
- `fix_notebook.py` - Notebook fixing utilities
- `sync_kaggle.py` - Helper script for Kaggle synchronization
- `git_workflow.ps1` - Automated Git workflow script
- `kernel-metadata.json` - Kaggle notebook metadata

## 🚀 Quick Start

### Setup Environment

See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for complete setup instructions.

### Sync with Kaggle

```powershell
# Download latest from Kaggle
python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training

# Push changes to Kaggle
python sync_kaggle.py push .

# List your notebooks
python sync_kaggle.py list
```

### Git Workflow

```powershell
# Quick commit and push
.\git_workflow.ps1 -message "Your commit message"
```

## 📚 Documentation

- [Environment Setup Guide](ENVIRONMENT_SETUP.md) - Complete setup for GitHub, Kaggle, and VS Code
- [Kaggle Notebook](https://www.kaggle.com/code/hemanthreganti/winner-trajectory-reward-grpo-training)

## 🛠️ Tools & Technologies

- **Python**: 3.14.0
- **Git**: 2.52.0
- **VS Code**: Latest
- **Kaggle API**: For notebook management
- **Jupyter**: For notebook development

## 👤 Author

Regantih (regantih@gmail.com)

## 🏆 Competition

Google Tunix Hackathon - Gemma Language Competition
