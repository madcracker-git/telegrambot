"""
Telegram Bot for NBA Scraper
Send game dates or queries to get NBA game results
"""

import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scraper import scrape_donbest, scrape_multiple_dates
import pandas as pd
import io

# Bot token - Set this as environment variable or replace with your token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8105630206:AAH2YrAHzvzZso4VRviVn819vQaFzMLoxUw")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    chat_type = update.message.chat.type
    
    if chat_type == "group" or chat_type == "supergroup":
        welcome_message = """
🏀 NBA Scraper Bot

I'm ready to help your group get NBA game results!

Commands:
/scrape YYYY-MM-DD - Scrape a single date
/range YYYY-MM-DD YYYY-MM-DD - Scrape date range
/game YYYY-MM-DD TEAM1 TEAM2 - Get specific game
/help - Show help

Examples:
• Send: 2025-10-31
• Send: /scrape 2025-10-31
• Send: /game 2025-10-31 ATL IND

I'll return:
✅ 1H scores (1H Total)
✅ 2H scores (2H Total)  
✅ OT points (OT Total)
✅ Full game data
"""
    else:
        welcome_message = """
🏀 NBA Scraper Bot

Send me NBA game dates and I'll get you the results!

Commands:
/start - Show this help message
/help - Show help
/scrape YYYY-MM-DD - Scrape a single date
/range YYYY-MM-DD YYYY-MM-DD - Scrape date range
/game YYYY-MM-DD TEAM1 TEAM2 - Get specific game

Examples:
• Send: 2025-10-31
• Send: /scrape 2025-10-31
• Send: /range 2025-10-01 2025-10-31
• Send: /game 2025-10-31 ATL IND

I'll return:
✅ 1H scores (1H Total)
✅ 2H scores (2H Total)  
✅ OT points (OT Total)
✅ Full game data
"""
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = """
📖 How to use:

1. Send a date (YYYY-MM-DD):
   Example: 2025-10-31

2. Use /scrape command:
   /scrape 2025-10-31

3. Scrape date range:
   /range 2025-10-01 2025-10-31

4. Get specific game:
   /game 2025-10-31 ATL IND

The bot will return:
• All games for that date
• 1H, 2H, and OT totals
• Excel file with full data
"""
    await update.message.reply_text(help_text)

async def scrape_date_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scrape command."""
    if not context.args:
        await update.message.reply_text("Usage: /scrape YYYY-MM-DD\nExample: /scrape 2025-10-31")
        return
    
    date_str = context.args[0]
    await scrape_and_send(update, context, date_str)

async def scrape_range_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /range command."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /range YYYY-MM-DD YYYY-MM-DD\nExample: /range 2025-10-01 2025-10-31")
        return
    
    start_date = context.args[0]
    end_date = context.args[1]
    
    await update.message.reply_text(f"Scraping dates from {start_date} to {end_date}...")
    
    try:
        from scraper import scrape_date_range
        df = scrape_date_range(start_date, end_date, combine_only=True)
        
        if df.empty:
            await update.message.reply_text("❌ No games found in that date range")
            return
        
        # Send summary
        summary = f"✅ Found {len(df)} games\n\n"
        summary += "Sample games:\n"
        for idx, row in df.head(5).iterrows():
            summary += f"• {row['Away Team']} @ {row['Home Team']}\n"
            summary += f"  1H: {row['1H Total']} | 2H: {row['2H Total']} | OT: {row['OT Total']}\n"
        
        await update.message.reply_text(summary)
        
        # Send Excel file
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        await update.message.reply_document(
            document=excel_buffer,
            filename=f"NBA_{start_date}_to_{end_date}.xlsx",
            caption=f"📊 {len(df)} games from {start_date} to {end_date}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def get_game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /game command to get specific game."""
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /game YYYY-MM-DD TEAM1 TEAM2\nExample: /game 2025-10-31 ATL IND")
        return
    
    date_str = context.args[0]
    team1 = context.args[1].upper()
    team2 = context.args[2].upper()
    
    await update.message.reply_text(f"Looking for {team1} @ {team2} on {date_str}...")
    
    try:
        df = scrape_donbest(date_str, save_file=False)
        
        if df.empty:
            await update.message.reply_text(f"❌ No games found for {date_str}")
            return
        
        # Find the game
        game = df[
            ((df["Away Team"] == team1) & (df["Home Team"] == team2)) |
            ((df["Away Team"] == team2) & (df["Home Team"] == team1))
        ]
        
        if game.empty:
            await update.message.reply_text(f"❌ Game {team1} @ {team2} not found on {date_str}")
            return
        
        g = game.iloc[0]
        away = g["Away Team"]
        home = g["Home Team"]
        
        result = f"🏀 {away} @ {home}\n"
        result += f"📅 {date_str}\n\n"
        result += f"1H: {away} {g['1H Away']} - {home} {g['1H Home']}\n"
        result += f"    Total: {g['1H Total']}\n\n"
        result += f"2H: {away} {g['2H Away']} - {home} {g['2H Home']}\n"
        result += f"    Total: {g['2H Total']}\n\n"
        result += f"Final: {away} {g['Final Away']} - {home} {g['Final Home']}\n"
        result += f"    Total: {g['Final Total']}\n\n"
        
        if g['OT Total'] > 0:
            result += f"OT: {away} {g['OT Away']} - {home} {g['OT Home']}\n"
            result += f"    Total: {g['OT Total']}\n"
        
        await update.message.reply_text(result)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def scrape_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE, date_str: str):
    """Scrape date and send results."""
    await update.message.reply_text(f"Scraping {date_str}...")
    
    try:
        df = scrape_donbest(date_str, save_file=False)
        
        if df.empty:
            await update.message.reply_text(f"❌ No games found for {date_str}")
            return
        
        # Send summary
        summary = f"✅ Found {len(df)} games on {date_str}\n\n"
        summary += "Games:\n"
        for idx, row in df.iterrows():
            # Validate scores before displaying
            if pd.isna(row['1H Total']) or row['1H Total'] < 50:
                # Skip games with invalid scores
                continue
            summary += f"• {row['Away Team']} @ {row['Home Team']}\n"
            summary += f"  1H: {int(row['1H Total'])} | 2H: {int(row['2H Total'])}"
            if row['OT Total'] > 0:
                summary += f" | OT: {int(row['OT Total'])}"
            summary += "\n"
        
        # Split if message is too long
        if len(summary) > 4000:
            # Send first part
            await update.message.reply_text(summary[:4000])
            # Send rest
            await update.message.reply_text(summary[4000:])
        else:
            await update.message.reply_text(summary)
        
        # Send Excel file
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        await update.message.reply_document(
            document=excel_buffer,
            filename=f"NBA_{date_str}.xlsx",
            caption=f"📊 {len(df)} games from {date_str}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    # Ignore messages that mention the bot in groups (unless it's a direct command)
    if update.message.chat.type in ["group", "supergroup"]:
        # Only respond if bot is mentioned or message starts with /
        if update.message.text and not update.message.text.startswith('/'):
            # Check if bot is mentioned
            bot_username = context.bot.username
            if bot_username and f"@{bot_username}" not in update.message.text:
                return
    
    text = update.message.text.strip()
    
    # Check if it's a date (YYYY-MM-DD format)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    date_match = re.search(date_pattern, text)
    
    if date_match:
        date_str = date_match.group(0)
        await scrape_and_send(update, context, date_str)
        return
    
    # Check if it's MM/DD format
    mmdd_pattern = r'\d{1,2}/\d{1,2}'
    mmdd_match = re.search(mmdd_pattern, text)
    
    if mmdd_match:
        mmdd = mmdd_match.group(0)
        try:
            # Convert to YYYY-MM-DD (assuming 2025)
            dt = datetime.strptime(f"2025/{mmdd}", "%Y/%m/%d")
            date_str = dt.strftime("%Y-%m-%d")
            await scrape_and_send(update, context, date_str)
            return
        except:
            pass
    
    # Check if it's a game query format: "MM/DD NBA GAME_ID: TEAM1 TEAM2"
    # Example: "10/24	NBA 546: SAS NOP" or "10/24 NBA 546: SAS NOP"
    # Handle various formats with tabs, spaces, @ symbols, etc.
    
    # First try: standard format
    game_query_pattern = r'(\d{1,2}/\d{1,2})[^\w]*NBA[^\w]*(\d+)[^\w]*:?[^\w@]*([A-Z]{3})[^\w@]+([A-Z]{3})'
    game_match = re.search(game_query_pattern, text, re.IGNORECASE)
    
    # Second try: handle @ symbols (e.g., "10/31 NBA 546: @ SAS")
    if not game_match:
        game_query_pattern2 = r'(\d{1,2}/\d{1,2})[^\w]*NBA[^\w]*(\d+)[^\w]*:?[^\w]*@?[^\w]*([A-Z]{3})[^\w@]+([A-Z]{3})'
        game_match = re.search(game_query_pattern2, text, re.IGNORECASE)
    
    # Third try: extract teams after colon, ignoring @ symbols
    if not game_match:
        # Find date and game ID first
        date_game_match = re.search(r'(\d{1,2}/\d{1,2})[^\w]*NBA[^\w]*(\d+)', text, re.IGNORECASE)
        if date_game_match:
            # Remove @ symbols and find team codes
            text_clean = re.sub(r'@+', ' ', text)
            # Find two 3-letter team codes after the colon
            teams_match = re.search(r':[^\w]*([A-Z]{3})[^\w]+([A-Z]{3})', text_clean, re.IGNORECASE)
            if teams_match:
                mmdd = date_game_match.group(1)
                game_id = date_game_match.group(2)
                team1 = teams_match.group(1).upper()
                team2 = teams_match.group(2).upper()
                # Create a fake match object
                class FakeMatch:
                    def __init__(self, groups_tuple):
                        self.groups_result = groups_tuple
                    def group(self, n):
                        return self.groups_result[n-1]
                game_match = FakeMatch((mmdd, game_id, team1, team2))
    
    if game_match:
        mmdd = game_match.group(1)
        game_id = game_match.group(2)
        team1 = game_match.group(3).upper().strip()
        team2 = game_match.group(4).upper().strip()
        
        # Clean team names - remove any special characters
        team1 = re.sub(r'[^A-Z]', '', team1)
        team2 = re.sub(r'[^A-Z]', '', team2)
        
        # Validate team abbreviations (3 letters) and check for @ symbols
        if '@' in team1 or '@' in team2 or len(team1) != 3 or len(team2) != 3:
            await update.message.reply_text(
                f"❌ Could not parse team names from: {text}\n\n"
                f"Please use format: MM/DD NBA GAME_ID: TEAM1 TEAM2\n"
                f"Example: 10/24 NBA 546: SAS NOP"
            )
            return
        
        # Check if teams are valid NBA teams
        nba_teams = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 
                     'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
                     'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
        
        if team1 not in nba_teams or team2 not in nba_teams:
            await update.message.reply_text(
                f"❌ Invalid team codes: {team1} or {team2}\n"
                f"Please use valid NBA team abbreviations (e.g., SAS, NOP, ATL, etc.)"
            )
            return
        
        try:
            dt = datetime.strptime(f"2025/{mmdd}", "%Y/%m/%d")
            date_str = dt.strftime("%Y-%m-%d")
            
            await update.message.reply_text(f"Looking for Game {game_id}: {team1} @ {team2} on {date_str}...")
            
            df = scrape_donbest(date_str, save_file=False)
            
            if df.empty:
                await update.message.reply_text(f"❌ No games found for {date_str}")
                return
            
            # Find the game - try both orders
            game = df[
                ((df["Away Team"] == team1) & (df["Home Team"] == team2)) |
                ((df["Away Team"] == team2) & (df["Home Team"] == team1))
            ]
            
            if game.empty:
                # Try to find similar games to help user
                available_games = df[df["Date"] == date_str]
                if not available_games.empty:
                    games_list = "\n".join([f"• {row['Away Team']} @ {row['Home Team']}" 
                                          for _, row in available_games.head(10).iterrows()])
                    await update.message.reply_text(
                        f"❌ Game {team1} @ {team2} not found on {date_str}\n\n"
                        f"Available games on {date_str}:\n{games_list}"
                    )
                else:
                    await update.message.reply_text(f"❌ Game {team1} @ {team2} not found on {date_str}")
                return
            
            g = game.iloc[0]
            away = g["Away Team"]
            home = g["Home Team"]
            
            result = f"🏀 Game {game_id}: {away} @ {home}\n"
            result += f"📅 {date_str}\n\n"
            result += f"1H: {away} {g['1H Away']} - {home} {g['1H Home']}\n"
            result += f"    Total: {g['1H Total']}\n\n"
            result += f"2H: {away} {g['2H Away']} - {home} {g['2H Home']}\n"
            result += f"    Total: {g['2H Total']}\n\n"
            result += f"Final: {away} {g['Final Away']} - {home} {g['Final Home']}\n"
            result += f"    Total: {g['Final Total']}\n\n"
            
            if g['OT Total'] > 0:
                result += f"OT: {away} {g['OT Away']} - {home} {g['OT Home']}\n"
                result += f"    Total: {g['OT Total']}\n"
            
            await update.message.reply_text(result)
            return
        except ValueError as e:
            await update.message.reply_text(f"❌ Invalid date format: {mmdd}\nPlease use MM/DD format (e.g., 10/24)")
            return
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            return
    
    # Default response
    await update.message.reply_text(
        "Please send:\n"
        "• A date (YYYY-MM-DD or MM/DD)\n"
        "• Game query (MM/DD NBA GAME_ID: TEAM1 TEAM2)\n"
        "• Or use commands:\n"
        "  /scrape YYYY-MM-DD\n"
        "  /range YYYY-MM-DD YYYY-MM-DD\n"
        "  /game YYYY-MM-DD TEAM1 TEAM2"
    )

def main():
    """Start the bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  Please set TELEGRAM_BOT_TOKEN environment variable")
        print("   Or edit telegram_bot.py and add your token")
        print("\nTo get a bot token:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot and follow instructions")
        print("3. Copy the token and set it as environment variable:")
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scrape", scrape_date_command))
    application.add_handler(CommandHandler("range", scrape_range_command))
    application.add_handler(CommandHandler("game", get_game_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    print("🤖 Bot is running...")
    print("Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

