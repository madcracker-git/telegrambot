# 🚀 Push to GitHub

Your code is committed! Now push it to GitHub.

## Push Command

Run this command:

```powershell
git push -u origin main
```

## Authentication

If GitHub asks for credentials:

### Option 1: Personal Access Token (Recommended)

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `nba-bot-push`
   - Select scopes: ✅ `repo` (all repo permissions)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)

2. **Use Token:**
   - Username: Your GitHub username
   - Password: Paste the token (not your GitHub password)

### Option 2: GitHub Desktop (Easier)

1. Download: https://desktop.github.com
2. Sign in with GitHub
3. Add your repository
4. Click "Push origin"

### Option 3: GitHub CLI

```powershell
gh auth login
gh repo sync
```

## After Pushing

✅ Your code will be on GitHub at:
**https://github.com/madcracker-git/telegrambot**

## Next: Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `madcracker-git/telegrambot`
6. Add environment variable: `TELEGRAM_BOT_TOKEN`
7. Your bot runs 24/7! 🎉

