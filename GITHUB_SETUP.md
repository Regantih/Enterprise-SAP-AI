# GitHub Repository Setup Commands

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `tunix-hackathon` (or your preferred name)
3. Choose **Private** or **Public**
4. **Do NOT** check "Initialize this repository with a README"
5. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```powershell
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/tunix-hackathon.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Example (Replace with your username):

```powershell
# If your GitHub username is "johndoe"
git remote add origin https://github.com/johndoe/tunix-hackathon.git
git branch -M main
git push -u origin main
```

## Authentication

When you push, GitHub will ask for authentication:

**Option 1: GitHub CLI (Recommended)**
```powershell
gh auth login
```

**Option 2: Personal Access Token**
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scopes: `repo` (full control of private repositories)
- Copy the token
- Use it as your password when pushing

## Verify Success

After pushing, you should see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/YOUR_USERNAME/tunix-hackathon.git
 * [new branch]      main -> main
```

## Future Pushes

After the initial setup, use the helper script:
```powershell
.\git_workflow.ps1 -message "Your commit message"
```

This will automatically add, commit, and push your changes!
