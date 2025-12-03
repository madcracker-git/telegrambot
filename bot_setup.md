# Telegram Bot Setup Guide

## Quick Start

1. **Get a Telegram Bot Token:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Copy the token you receive

2. **Set the Token:**
   
   **Option A - Environment Variable (Recommended):**
   ```bash
   # Windows PowerShell
   $env:TELEGRAM_BOT_TOKEN="your_token_here"
   
   # Windows CMD
   set TELEGRAM_BOT_TOKEN=your_token_here
   
   # Linux/Mac
   export TELEGRAM_BOT_TOKEN="your_token_here"
   ```
   
   **Option B - Edit the file:**
   - Open `telegram_bot.py`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual token

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Bot:**
   ```bash
   python telegram_bot.py
   ```

5. **Use the Bot:**
   - Open Telegram and search for your bot (the name you gave it)
   - Send `/start` to see commands
   - Send a date like `2025-10-31` to get games

## Bot Commands

- `/start` - Show help message
- `/help` - Show help
- `/scrape YYYY-MM-DD` - Scrape a single date
- `/range YYYY-MM-DD YYYY-MM-DD` - Scrape date range
- `/game YYYY-MM-DD TEAM1 TEAM2` - Get specific game

## Examples

**Send a date:**
```
2025-10-31
```

**Use command:**
```
/scrape 2025-10-31
```

**Get specific game:**
```
/game 2025-10-31 ATL IND
```

**Scrape date range:**
```
/range 2025-10-01 2025-10-31
```

## What the Bot Returns

✅ Game results with:
- 1H scores (1H Total)
- 2H scores (2H Total)
- OT points (OT Total)
- Full game data

✅ Excel file with all data

