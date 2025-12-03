# 📱 How to Add Bot to Group Chat

## Step-by-Step Instructions

### 1. Add Bot to Your Group

1. **Open Telegram** and go to your group chat

2. **Click on the group name** at the top to open group info

3. **Click "Add Members"** or the **"+"** button

4. **Search for your bot** by its username (the name you gave it when creating with @BotFather)

5. **Select your bot** and click "Add"

### 2. Give Bot Permissions (Important!)

After adding the bot, make sure it has permissions:

1. Go to **Group Settings** → **Administrators**

2. Find your bot and click on it

3. Make sure these permissions are enabled:
   - ✅ **Read Messages** (must have)
   - ✅ **Send Messages** (must have)
   - ✅ **Send Media** (needed for Excel files)

### 3. Use Bot in Group

**Option A - Mention the bot:**
```
@your_bot_name 2025-10-31
```

**Option B - Use commands (no mention needed):**
```
/scrape 2025-10-31
/game 2025-10-31 ATL IND
```

**Option C - Just send date (if bot is set to respond to all messages):**
```
2025-10-31
```

## Bot Commands for Groups

- `/scrape YYYY-MM-DD` - Get games for a date
- `/range YYYY-MM-DD YYYY-MM-DD` - Get games for date range
- `/game YYYY-MM-DD TEAM1 TEAM2` - Get specific game
- `/help` - Show help message

## Example Usage in Group

**User sends:**
```
/scrape 2025-10-31
```

**Bot responds:**
```
✅ Found 9 games on 2025-10-31

Games:
• ATL @ IND
  1H: 122 | 2H: 114 | OT: 0
• TOR @ CLE
  1H: 91 | 2H: 122 | OT: 0
...
[Excel file attached]
```

## Troubleshooting

**Bot not responding?**
- Make sure bot has "Read Messages" permission
- Try mentioning the bot: `@your_bot_name 2025-10-31`
- Use commands instead: `/scrape 2025-10-31`

**Bot can't send files?**
- Enable "Send Media" permission in group settings
- Make sure bot is not restricted

**Bot responds to everything?**
- The bot is configured to respond when mentioned or when commands are used
- To change this, edit `telegram_bot.py` and modify the `handle_message` function

## Privacy Note

The bot will only respond to:
- Commands (starting with `/`)
- Messages that mention the bot (`@your_bot_name`)
- Direct messages (if someone DMs the bot)

This prevents spam in your group!

