# 📦 GitHub Setup Guide

## Step 1: Configure Git (One-time setup)

Run these commands with YOUR information:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)

1. **Go to GitHub:**
   - Visit https://github.com
   - Sign in (or create account)

2. **Create New Repository:**
   - Click the **"+"** icon (top right)
   - Click **"New repository"**
   - Repository name: `nba-scraper-bot` (or any name you like)
   - Description: "NBA Scraper Telegram Bot"
   - Choose **Public** or **Private**
   - **DO NOT** check "Initialize with README" (we already have files)
   - Click **"Create repository"**

3. **Copy the repository URL:**
   - You'll see a page with commands
   - Copy the URL (looks like: `https://github.com/yourusername/nba-scraper-bot.git`)

### Option B: Using GitHub CLI (if installed)

```powershell
gh repo create nba-scraper-bot --public --source=. --remote=origin --push
```

## Step 3: Connect and Push to GitHub

After creating the repo, run these commands:

```powershell
# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Commit your files
git commit -m "Initial commit: NBA Scraper Telegram Bot"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Verify

- Go to your GitHub repository page
- You should see all your files there!

## Next: Deploy to Railway

After pushing to GitHub:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Add environment variable: `TELEGRAM_BOT_TOKEN`
7. Done! Bot runs 24/7 🚀

---

## Troubleshooting

**If you get authentication error:**
- GitHub now requires Personal Access Token (not password)
- Go to: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with `repo` permissions
- Use token as password when pushing

**If files are already committed:**
- Your files are already staged
- Just need to add remote and push!

