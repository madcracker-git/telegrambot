# 🚀 Free Hosting Guide for Telegram Bot

## Option 1: Railway (Recommended - Easiest)

### Steps:

1. **Sign up at Railway:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository (or create one)

3. **Add Environment Variable:**
   - Go to your project → Variables
   - Add: `TELEGRAM_BOT_TOKEN` = `your_bot_token`

4. **Configure Build:**
   - Railway auto-detects Python
   - Add `Procfile` (see below)

5. **Deploy:**
   - Railway will auto-deploy
   - Bot runs 24/7 for free!

### Files Needed:

**Procfile** (create in root):
```
worker: python telegram_bot.py
```

**runtime.txt** (optional, specify Python version):
```
python-3.11
```

---

## Option 2: Render (Also Easy)

### Steps:

1. **Sign up at Render:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select your repository

3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python telegram_bot.py`
   - **Environment:** Python 3

4. **Add Environment Variable:**
   - Go to Environment
   - Add: `TELEGRAM_BOT_TOKEN` = `your_bot_token`

5. **Deploy:**
   - Click "Create Web Service"
   - Bot runs 24/7!

**Note:** Render free tier sleeps after 15 min inactivity. Use Railway for always-on.

---

## Option 3: PythonAnywhere (Free Tier)

### Steps:

1. **Sign up:**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Files:**
   - Go to Files tab
   - Upload all your Python files
   - Upload `requirements.txt`

3. **Install Dependencies:**
   - Go to Bash console
   - Run: `pip3.10 install --user -r requirements.txt`

4. **Set Environment Variable:**
   - In Bash: `export TELEGRAM_BOT_TOKEN="your_token"`

5. **Create Scheduled Task:**
   - Go to Tasks tab
   - Create task: `python3.10 telegram_bot.py`
   - Set to run "every day"

**Note:** Free tier has limited CPU time, but works for bots.

---

## Option 4: Replit (Free but Less Reliable)

### Steps:

1. **Go to Replit:**
   - https://replit.com
   - Sign up

2. **Create Python Repl:**
   - Click "Create Repl"
   - Choose Python

3. **Upload Files:**
   - Upload all your files
   - Install packages: `pip install -r requirements.txt`

4. **Set Secrets:**
   - Go to Secrets tab
   - Add: `TELEGRAM_BOT_TOKEN` = `your_token`

5. **Run:**
   - Click Run button
   - Bot runs while tab is open

**Note:** Free tier stops when tab closes. Use "Always On" (paid) or keep tab open.

---

## Option 5: Fly.io (Free Tier)

### Steps:

1. **Install Fly CLI:**
   ```bash
   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up:**
   ```bash
   fly auth signup
   ```

3. **Create App:**
   ```bash
   fly launch
   ```

4. **Set Secret:**
   ```bash
   fly secrets set TELEGRAM_BOT_TOKEN="your_token"
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

---

## 🎯 Recommended: Railway

**Why Railway?**
- ✅ Always-on (doesn't sleep)
- ✅ Easy setup
- ✅ Free tier: 500 hours/month
- ✅ Auto-deploys from GitHub
- ✅ Simple environment variables

**Free Tier Limits:**
- 500 hours/month (enough for 24/7)
- $5 credit monthly

---

## 📝 Quick Setup for Railway

1. Create `Procfile` in your project root:
   ```
   worker: python telegram_bot.py
   ```

2. Push to GitHub

3. Connect Railway to GitHub

4. Add environment variable: `TELEGRAM_BOT_TOKEN`

5. Deploy!

Your bot will run 24/7 for free! 🎉

