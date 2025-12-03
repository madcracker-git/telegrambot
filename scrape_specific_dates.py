"""
Script to scrape specific NBA game dates from the user's list.
Converts MM/DD format to YYYY-MM-DD and scrapes all dates.
All results are combined into ONE Excel file.
"""

from scraper import scrape_multiple_dates
from datetime import datetime

# List of dates from user (MM/DD format, 2025 season)
dates_to_scrape = [
    "10/23", "10/24", "10/27", "10/29", "10/31",
    "11/1", "11/2", "11/3", "11/5", "11/7", "11/8", "11/9", "11/10", "11/11", "11/12", 
    "11/14", "11/15", "11/16", "11/17", "11/18", "11/19", "11/20", "11/21", "11/22", 
    "11/23", "11/24", "11/26", "11/28", "11/29", "11/30",
    "12/1"
]

def convert_date(date_str, year=2025):
    """Convert MM/DD to YYYY-MM-DD"""
    try:
        dt = datetime.strptime(f"{year}/{date_str}", "%Y/%m/%d")
        return dt.strftime("%Y-%m-%d")
    except:
        return None

if __name__ == "__main__":
    print("🏀 Scraping specific NBA game dates (2025 season)...\n")
    print("📝 All results will be combined into ONE Excel file\n")
    
    # Convert dates to YYYY-MM-DD format
    date_list = []
    for date_mmddyy in dates_to_scrape:
        # Use 2025 year
        date_2025 = convert_date(date_mmddyy, 2025)
        
        if date_2025:
            date_list.append(date_2025)
    
    # Use the new function that combines everything
    scrape_multiple_dates(date_list, output_filename="NBA_all_games.xlsx")
    
    print(f"\n{'='*60}")
    print("✅ Done! All results saved to: NBA_all_games.xlsx")

