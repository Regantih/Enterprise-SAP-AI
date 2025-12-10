# Kaggle Auto-Push Setup Guide

This guide will help you set up automatic notebook pushing to Kaggle.

## One-Time Setup

### Step 1: Get Your Kaggle API Credentials

1. Go to https://www.kaggle.com/settings/account
2. Scroll down to **API** section
3. Click **Create New Token**
4. This downloads `kaggle.json` to your Downloads folder

### Step 2: Install Kaggle Credentials

**Windows:**
```powershell
# Create .kaggle directory in your user folder
mkdir $env:USERPROFILE\.kaggle

# Move the downloaded kaggle.json there
move $env:USERPROFILE\Downloads\kaggle.json $env:USERPROFILE\.kaggle\

# Verify it's there
cat $env:USERPROFILE\.kaggle\kaggle.json
```

### Step 3: Test the Setup

Run this command to verify:
```powershell
python push_to_kaggle.py
```

## Future Usage

Once set up, whenever you have a fixed notebook:

1. Make sure the notebook file is in the same directory as `push_to_kaggle.py`
2. Edit `push_to_kaggle.py` if needed (change `NOTEBOOK_FILE` variable)
3. Run: `python push_to_kaggle.py`

That's it! The notebook will be automatically pushed to Kaggle.

## Troubleshooting

**Error: "Could not find kaggle.json"**
- Make sure `kaggle.json` is in `C:\Users\hrega\.kaggle\`

**Error: "401 Unauthorized"**
- Your API token might be expired. Generate a new one from Kaggle settings.

**Error: "Kernel not found"**
- Update the `KERNEL_SLUG` in `push_to_kaggle.py` to match your notebook's slug.
