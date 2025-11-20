# Kaggle API Token Issue - Resolution Guide

## 🔍 Issue Identified

The Kaggle API credentials (`kaggle.json`) are configured correctly, but API calls return:
```
401 Client Error: Unauthorized
```

## ✅ What's Working
- ✅ Kaggle package installed (v1.7.4.5)
- ✅ `kaggle.json` in correct location (`C:\Users\hrega\.kaggle\kaggle.json`)
- ✅ API authentication initializes successfully
- ❌ API calls fail with 401 Unauthorized

## 🔧 Solution: Regenerate API Token

The API token in your `kaggle.json` file appears to be invalid or expired. You need to generate a new one:

### Steps to Fix:

1. **Go to Kaggle Settings**
   - Open: https://www.kaggle.com/settings
   - Log in if needed

2. **Revoke Old Token (Optional but Recommended)**
   - Scroll to the **API** section
   - If there's an existing token, click **"Expire API Token"**

3. **Create New Token**
   - Click **"Create New API Token"**
   - This will download a new `kaggle.json` file

4. **Replace the Old File**
   Run these commands in PowerShell:
   ```powershell
   # Move the new kaggle.json (it will overwrite the old one)
   Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$env:USERPROFILE\.kaggle\kaggle.json" -Force
   ```

5. **Test the New Token**
   ```powershell
   python test_kaggle.py
   ```

   Or test directly:
   ```powershell
   python sync_kaggle.py list
   ```

## 📝 Why This Happens

- API tokens can expire
- Tokens may be invalidated if regenerated on Kaggle's website
- Security settings changes on Kaggle account

## ✅ Expected Output After Fix

```
✅ Kaggle import successful
✅ Authentication successful
✅ Found X notebooks
  - Notebook 1 Title
  - Notebook 2 Title
  ...
```

## 🚀 Next Steps After Fix

Once the token is working:

1. **Download your GRPO notebook:**
   ```powershell
   python sync_kaggle.py download hemanthreganti/winner-trajectory-reward-grpo-training
   ```

2. **Continue with GitHub setup** (if not done yet)

---

**Need Help?** If regenerating the token doesn't work, check:
- You're logged into the correct Kaggle account
- Your Kaggle account has API access enabled
- No firewall/proxy blocking Kaggle API requests
