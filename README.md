# 🏀 NBA Scraper Telegram Bot

A Telegram bot that scrapes NBA game scores from DonBest and provides 1H, 2H, and OT totals.

## Features

- ✅ Scrapes NBA scores from DonBest
- ✅ Returns 1H, 2H, and OT totals
- ✅ Sends Excel files with full game data
- ✅ Works in groups and private chats
- ✅ Multiple query formats supported

## Quick Start

### Local Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set bot token:**
   ```bash
   # Windows PowerShell
   $env:TELEGRAM_BOT_TOKEN="your_token_here"
   
   # Linux/Mac
   export TELEGRAM_BOT_TOKEN="your_token_here"
   ```

3. **Run bot:**
   ```bash
   python telegram_bot.py
   ```

### Free Hosting (Railway - Recommended)

1. **Sign up:** https://railway.app
2. **Connect GitHub repo**
3. **Add environment variable:** `TELEGRAM_BOT_TOKEN`
4. **Deploy!**

See `HOSTING_GUIDE.md` for detailed instructions.

## Bot Commands

- `/start` - Show help
- `/scrape YYYY-MM-DD` - Scrape single date
- `/range YYYY-MM-DD YYYY-MM-DD` - Scrape date range
- `/game YYYY-MM-DD TEAM1 TEAM2` - Get specific game

## Usage Examples

**Send a date:**
```
2025-10-31
```

**Game query:**
```
10/24 NBA 546: SAS NOP
```

**Command:**
```
/scrape 2025-10-31
```

## Files

- `telegram_bot.py` - Main bot code
- `scraper.py` - Scraper functions
- `requirements.txt` - Python dependencies
- `Procfile` - For Railway/Render hosting
- `HOSTING_GUIDE.md` - Free hosting instructions

## License

MIT
