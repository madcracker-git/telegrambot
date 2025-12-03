import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, timedelta
import sys


def scrape_donbest(date, debug=False, save_file=True):
    """
    Scrape NBA scores from DonBest for a specific date.
    
    Args:
        date: Date string in format YYYY-MM-DD
        debug: If True, print debug information
        save_file: If True, save individual Excel file for this date
        
    Returns:
        DataFrame with scraped game data
    """
    url = f"http://server1.donbest.com/scores/{date}/all.html"
    print(f"Fetching: {url}")

    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            raise Exception(f"Error fetching page: Status code {r.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")

    soup = BeautifulSoup(r.text, "html.parser")
    rows = []
    
    if debug:
        # Save HTML for inspection
        with open(f"debug_{date}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Debug HTML saved to debug_{date}.html")
    
    # NBA team abbreviations and full names mapping
    nba_teams = {
        'ATL': 'Atlanta', 'BOS': 'Boston', 'BKN': 'Brooklyn', 'CHA': 'Charlotte', 
        'CHI': 'Chicago', 'CLE': 'Cleveland', 'DAL': 'Dallas', 'DEN': 'Denver', 
        'DET': 'Detroit', 'GSW': 'Golden State', 'HOU': 'Houston', 'IND': 'Indiana',
        'LAC': 'LA Clippers', 'LAL': 'LA Lakers', 'MEM': 'Memphis', 'MIA': 'Miami',
        'MIL': 'Milwaukee', 'MIN': 'Minnesota', 'NOP': 'New Orleans', 'NYK': 'New York',
        'OKC': 'Oklahoma City', 'ORL': 'Orlando', 'PHI': 'Philadelphia', 'PHX': 'Phoenix',
        'POR': 'Portland', 'SAC': 'Sacramento', 'SAS': 'San Antonio', 'TOR': 'Toronto',
        'UTA': 'Utah', 'WAS': 'Washington'
    }
    
    # Find all table rows that contain NBA games
    # DonBest structure: Each game has 2 rows (away team, home team)
    # Each row contains: Game ID, Team, Q1, Q2, Q3, Q4, Total, 1H, 2H, betting lines
    # Structure: <td>GameID</td><td>Team</td><td>Q1</td><td>Q2</td><td>Q3</td><td>Q4</td><td>Total</td><td>F?</td><td>1H</td><td>2H</td>...
    
    # Find NBA section by looking for NBA headers
    all_rows = soup.find_all("tr")
    nba_rows = []
    in_nba_section = False
    
    if debug:
        print(f"  🔍 Found {len(all_rows)} total table rows")
    
    # Find rows that are in NBA section
    for row in all_rows:
        cells = row.find_all(["td", "th"])
        if len(cells) < 5:
            continue
        
        cell_texts = [cell.get_text(" ", strip=True) for cell in cells]
        full_text = " ".join(cell_texts).upper()
        
        # Check if this is an NBA section header
        if "NBA" in full_text and ("FRIDAY" in full_text or "THURSDAY" in full_text or 
                                   "SATURDAY" in full_text or "SUNDAY" in full_text or 
                                   "MONDAY" in full_text or "TUESDAY" in full_text or 
                                   "WEDNESDAY" in full_text):
            in_nba_section = True
            if debug:
                print(f"  📍 Found NBA section header")
            continue
        
        # If we hit another sport section, stop NBA section
        if in_nba_section:
            if ("COLLEGE" in full_text and "BASKETBALL" in full_text) or \
               ("NCAA" in full_text) or \
               ("ABA" in full_text and "LEAGUE" in full_text) or \
               (any(sport in full_text for sport in ["MLB", "NHL", "NFL", "SOCCER", "TENNIS"])):
                in_nba_section = False
                continue
        
        # If we're in NBA section, check if this row contains an NBA team
        if in_nba_section:
            # Check if this row has a game ID (first cell should be a number)
            first_cell = cell_texts[0].strip() if cell_texts else ""
            if first_cell.isdigit() or re.match(r'^\d{3,4}$', first_cell):
                # Check if second cell contains an NBA team
                second_cell = cell_texts[1].strip() if len(cell_texts) > 1 else ""
                for abbr, full_name in nba_teams.items():
                    if (abbr == second_cell.upper() or 
                        full_name.upper() == second_cell.upper() or
                        (abbr in second_cell.upper() and len(second_cell) < 25)):
                        nba_rows.append(row)
                        if debug:
                            print(f"  ✅ Found NBA row: {abbr} (Game ID: {first_cell})")
                        break
    
    if debug:
        print(f"  📊 Found {len(nba_rows)} NBA game rows")
    
    if not nba_rows:
        print("  ⚠️  Could not find NBA games in HTML")
        return pd.DataFrame()
    
    game_data = {}  # Store game data by game ID pair
    current_game_pair = None
    
    # Process NBA rows
    for row in nba_rows:
        cells = row.find_all(["td", "th"])
        if len(cells) < 10:
            continue
        
        # Get text from all cells
        cell_texts = [cell.get_text(" ", strip=True) for cell in cells]
        full_text = " ".join(cell_texts).upper()
        
        # Skip header rows - they contain "1 2 3 4" or time patterns like "4:10pm"
        if len(cell_texts) > 2:
            # Check if first cell contains time pattern AND column headers (header row)
            if re.search(r'\d{1,2}:\d{2}[ap]m', cell_texts[0]) and "1" in cell_texts[2] and "2" in cell_texts[3] and "3" in cell_texts[4]:
                continue
            # Check if it's a header row with column labels
            if "OPEN" in full_text and "CLOSE" in full_text and "ATS" in full_text and len(cell_texts) > 10:
                # Make sure it's actually a header (has "1H" and "2H" as labels, not scores)
                if "1H" in cell_texts[7] or "2H" in cell_texts[8]:
                    continue
        
        # Try to find game ID (first cell should contain just game ID number)
        game_id = None
        if cell_texts[0] and cell_texts[0].strip().isdigit():
            game_id = cell_texts[0].strip()
        else:
            # Try to extract from first cell
            game_id_match = re.search(r'^\s*(\d{3,4})\s*$', cell_texts[0])
            if game_id_match:
                game_id = game_id_match.group(1)
        
        if not game_id:
            continue
        
        # Make sure this is actually an NBA game row, not another sport
        # NBA games should have 4 quarter scores, not periods/innings
        if len(cell_texts) < 10:
            continue
        
        # Find team name (second cell usually contains team name)
        team_abbr = None
        team_name = None
        
        team_cell = cell_texts[1] if len(cell_texts) > 1 else ""
        team_cell_upper = team_cell.upper().strip()
        
        # Check if this is actually an NBA team
        # First try exact matches
        for abbr, full_name in nba_teams.items():
            full_name_upper = full_name.upper()
            
            # Exact abbreviation match
            if abbr == team_cell_upper:
                team_abbr = abbr
                team_name = full_name
                break
            
            # Exact full name match
            if full_name_upper == team_cell_upper:
                team_abbr = abbr
                team_name = full_name
                break
        
        # If no exact match, try partial matches (but only in NBA context)
        if not team_abbr:
            for abbr, full_name in nba_teams.items():
                full_name_upper = full_name.upper()
                
                # Check if full name is contained in team cell (e.g., "Golden State" in "Golden State")
                if full_name_upper in team_cell_upper:
                    if len(team_cell_upper) < 30:  # Reasonable length
                        team_abbr = abbr
                        team_name = full_name
                        break
                
                # Check if abbreviation appears as whole word
                if re.search(r'\b' + re.escape(abbr) + r'\b', team_cell_upper):
                    if len(team_cell_upper) < 25:
                        team_abbr = abbr
                        team_name = full_name
                        break
        
        if not team_abbr:
            continue
        
        # Extract scores from cells
        # Structure varies:
        # Normal: [GameID, Team, Q1, Q2, Q3, Q4, Total, F, 1H, 2H, ...]
        # With OT: [GameID, Team, Q1, Q2, Q3, Q4, OT_points, Total, OT_indicator, 1H, 2H, ...]
        # Index:   0       1     2   3   4   5   6          7      8             9   10
        
        try:
            # Parse quarter scores directly from cells 2, 3, 4, 5
            q1 = int(cell_texts[2]) if len(cell_texts) > 2 and cell_texts[2].strip().isdigit() else None
            q2 = int(cell_texts[3]) if len(cell_texts) > 3 and cell_texts[3].strip().isdigit() else None
            q3 = int(cell_texts[4]) if len(cell_texts) > 4 and cell_texts[4].strip().isdigit() else None
            q4 = int(cell_texts[5]) if len(cell_texts) > 5 and cell_texts[5].strip().isdigit() else None
            
            # Check cell 6 and cell 7/8 for OT indicators
            cell6_text = cell_texts[6].strip().upper() if len(cell_texts) > 6 else ""
            cell7_text = cell_texts[7].strip().upper() if len(cell_texts) > 7 else ""
            cell8_text = cell_texts[8].strip().upper() if len(cell_texts) > 8 else ""
            
            # Determine if this game has OT
            # If cell 6 is a small number (OT points) and cell 7 is total, then OT
            # Or if cell 7/8 contains "OT"
            has_ot = False
            ot_points = 0
            
            # Check if cell 6 looks like OT points (small number, 1-20 range typically)
            if len(cell_texts) > 6:
                cell6_val = cell_texts[6].strip()
                if cell6_val.isdigit() and 1 <= int(cell6_val) <= 30:
                    # Check if cell 7 is a larger number (total score)
                    if len(cell_texts) > 7:
                        cell7_val = cell_texts[7].strip()
                        if cell7_val.isdigit() and int(cell7_val) >= 80:
                            # This looks like OT structure: Q1-Q4, OT_points, Total
                            has_ot = True
                            ot_points = int(cell6_val)
            
            # Also check for OT indicator in cells 7-8
            if not has_ot and ("OT" in cell7_text or "OT" in cell8_text):
                has_ot = True
                # Try to get OT points from cell 6
                if len(cell_texts) > 6:
                    ot_text = cell_texts[6].strip()
                    if ot_text.isdigit():
                        ot_points = int(ot_text)
            
            # Parse total score - depends on whether there's OT
            total_score = None
            if has_ot:
                # With OT: Total is in cell 7
                if len(cells) > 7:
                    total_text = cells[7].get_text(strip=True)
                    total_match = re.search(r'\b(\d{2,3})\b', total_text)
                    if total_match:
                        total_score = int(total_match.group(1))
            else:
                # Normal: Total is in cell 6
                if len(cells) > 6:
                    total_text = cells[6].get_text(strip=True)
                    total_match = re.search(r'\b(\d{2,3})\b', total_text)
                    if total_match:
                        total_score = int(total_match.group(1))
            
            # Parse 1H and 2H - position depends on OT
            first_half = None
            second_half = None
            
            if has_ot:
                # With OT: 1H is in cell 9, 2H is in cell 10
                if len(cell_texts) > 9:
                    cell9_text = cell_texts[9].strip()
                    if cell9_text.isdigit():
                        first_half = int(cell9_text)
                
                if len(cell_texts) > 10:
                    cell10_text = cell_texts[10].strip()
                    if cell10_text.isdigit():
                        second_half = int(cell10_text)
            else:
                # Normal: 1H is in cell 8, 2H is in cell 9
                if len(cell_texts) > 8:
                    cell8_text = cell_texts[8].strip()
                    if cell8_text.isdigit():
                        first_half = int(cell8_text)
                
                if len(cell_texts) > 9:
                    cell9_text = cell_texts[9].strip()
                    if cell9_text.isdigit():
                        second_half = int(cell9_text)
            
            # Calculate missing values (only if not found)
            if first_half is None and q1 is not None and q2 is not None:
                first_half = q1 + q2
            
            if second_half is None and q3 is not None and q4 is not None:
                second_half = q3 + q4
            
            if total_score is None and q1 is not None and q2 is not None and q3 is not None and q4 is not None:
                total_score = q1 + q2 + q3 + q4
            
            # Validation
            if not all([q1 is not None, q2 is not None, q3 is not None, q4 is not None, total_score is not None]):
                if debug:
                    print(f"  ⚠️  Skipping {team_abbr} - missing scores: Q1={q1}, Q2={q2}, Q3={q3}, Q4={q4}, Total={total_score}")
                continue
            
        except (ValueError, IndexError) as e:
            if debug:
                print(f"  ⚠️  Error parsing scores for {team_abbr}: {e}")
            continue
        
        # Group games by consecutive game IDs (each game has 2 rows with sequential IDs)
        # Store by the first game ID of the pair
        if current_game_pair is None:
            current_game_pair = game_id
            game_data[current_game_pair] = {
                'away_team': team_abbr,
                'away_q1': q1,
                'away_q2': q2,
                'away_q3': q3,
                'away_q4': q4,
                'away_total': total_score,
                'away_1h': first_half,
                'away_2h': second_half,
                'away_has_ot': has_ot,
                'away_ot_points': ot_points
            }
        else:
            # Check if this is the second team of the same game (consecutive IDs)
            prev_id = int(current_game_pair)
            curr_id = int(game_id)
            
            if curr_id == prev_id + 1:
                # Same game, add home team
                game_data[current_game_pair]['home_team'] = team_abbr
                game_data[current_game_pair]['home_q1'] = q1
                game_data[current_game_pair]['home_q2'] = q2
                game_data[current_game_pair]['home_q3'] = q3
                game_data[current_game_pair]['home_q4'] = q4
                game_data[current_game_pair]['home_total'] = total_score
                game_data[current_game_pair]['home_1h'] = first_half
                game_data[current_game_pair]['home_2h'] = second_half
                game_data[current_game_pair]['home_has_ot'] = has_ot
                game_data[current_game_pair]['home_ot_points'] = ot_points
                current_game_pair = None  # Reset for next game
            else:
                # New game, start new pair
                current_game_pair = game_id
                game_data[current_game_pair] = {
                    'away_team': team_abbr,
                    'away_q1': q1,
                    'away_q2': q2,
                    'away_q3': q3,
                    'away_q4': q4,
                    'away_total': total_score,
                    'away_1h': first_half,
                    'away_2h': second_half,
                    'away_has_ot': has_ot,
                    'away_ot_points': ot_points
                }
    
    # Process collected game data
    for game_id, game in game_data.items():
        if 'away_team' not in game or 'home_team' not in game:
            continue
        
        try:
            # Get scores - use actual values from table, don't calculate
            away_1h = game.get('away_1h')
            home_1h = game.get('home_1h')
            away_total = game.get('away_total')
            home_total = game.get('home_total')
            away_2h = game.get('away_2h')  # This includes OT if game went to OT
            home_2h = game.get('home_2h')  # This includes OT if game went to OT
            
            # Fallback to calculation only if values are None
            if away_1h is None:
                away_1h = (game.get('away_q1', 0) + game.get('away_q2', 0)) or None
            if home_1h is None:
                home_1h = (game.get('home_q1', 0) + game.get('home_q2', 0)) or None
            if away_total is None:
                away_total = (game.get('away_q1', 0) + game.get('away_q2', 0) + game.get('away_q3', 0) + game.get('away_q4', 0)) or None
            if home_total is None:
                home_total = (game.get('home_q1', 0) + game.get('home_q2', 0) + game.get('home_q3', 0) + game.get('home_q4', 0)) or None
            if away_2h is None:
                away_2h = (game.get('away_q3', 0) + game.get('away_q4', 0)) or None
            if home_2h is None:
                home_2h = (game.get('home_q3', 0) + game.get('home_q4', 0)) or None
            
            # Calculate OT - check if game went to OT
            away_regulation = game.get('away_q1', 0) + game.get('away_q2', 0) + game.get('away_q3', 0) + game.get('away_q4', 0)
            home_regulation = game.get('home_q1', 0) + game.get('home_q2', 0) + game.get('home_q3', 0) + game.get('home_q4', 0)
            
            # Check OT indicators and OT points
            has_ot = game.get('away_has_ot', False) or game.get('home_has_ot', False)
            away_ot_points = game.get('away_ot_points', 0) or 0
            home_ot_points = game.get('home_ot_points', 0) or 0
            
            if has_ot:
                # Use OT points from table if available
                if away_ot_points > 0 or home_ot_points > 0:
                    ot_away = away_ot_points
                    ot_home = home_ot_points
                else:
                    # Calculate from difference
                    ot_away = max((away_total or 0) - away_regulation, 0)
                    ot_home = max((home_total or 0) - home_regulation, 0)
            elif (away_total and away_total > away_regulation) or (home_total and home_total > home_regulation):
                # OT detected by score difference
                ot_away = max((away_total or 0) - away_regulation, 0)
                ot_home = max((home_total or 0) - home_regulation, 0)
            else:
                ot_away = 0
                ot_home = 0
            
            # Validate we have all required values
            if away_1h is None or home_1h is None or away_total is None or home_total is None or away_2h is None or home_2h is None:
                if debug:
                    print(f"  ⚠️  Skipping game {game_id} - missing required scores")
                continue
            
            # Calculate totals
            first_half_total = away_1h + home_1h
            second_half_total = away_2h + home_2h
            ot_total = ot_away + ot_home
            
            rows.append({
                "Date": date,
                "Away Team": game['away_team'],
                "Home Team": game['home_team'],
                "1H Away": away_1h,
                "1H Home": home_1h,
                "1H Total": first_half_total,
                "Final Away": away_total,
                "Final Home": home_total,
                "Final Total": away_total + home_total,
                "2H Away": away_2h,
                "2H Home": home_2h,
                "2H Total": second_half_total,
                "OT Away": ot_away,
                "OT Home": ot_home,
                "OT Total": ot_total
            })
            
            if debug:
                print(f"  ✅ Game {game_id}: {game['away_team']} @ {game['home_team']}")
                print(f"     1H: {away_1h}-{home_1h}, Final: {away_total}-{home_total}, 2H: {away_2h}-{home_2h}, OT: {ot_away}-{ot_home}")
        
        except Exception as e:
            if debug:
                print(f"  ❌ Error processing game {game_id}: {e}")
            continue

    if not rows:
        print(f"❌ No NBA games found for {date}")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    
    # Save individual file if requested
    if save_file and len(rows) > 0:
        filename = f"NBA_{date}.xlsx"
        df.to_excel(filename, index=False)
        print(f"✅ Saved → {filename} ({len(rows)} games)")
    
    if len(rows) > 0:
        print(f"   📊 Games found: {len(rows)}")
        if len(rows) > 0:
            print(f"   📈 Sample: {rows[0]['Away Team']} @ {rows[0]['Home Team']}")

    return df


def scrape_date_range(start_date, end_date, combine_only=False):
    """
    Scrape NBA scores for a range of dates.
    
    Args:
        start_date: Start date string in format YYYY-MM-DD
        end_date: End date string in format YYYY-MM-DD
        combine_only: If True, only save combined file, not individual files
        
    Returns:
        Combined DataFrame with all games
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    all_games = []
    current = start
    
    print(f"\n📅 Scraping dates from {start_date} to {end_date}\n")
    if combine_only:
        print("📝 All results will be combined into ONE file\n")
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        try:
            df = scrape_donbest(date_str, save_file=not combine_only)
            if not df.empty:
                all_games.append(df)
        except Exception as e:
            print(f"❌ Error scraping {date_str}: {e}")
        
        current += timedelta(days=1)
    
    if not all_games:
        print("\n❌ No games found in the specified date range")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_games, ignore_index=True)
    filename = f"NBA_{start_date}_to_{end_date}.xlsx"
    combined_df.to_excel(filename, index=False)
    print(f"\n{'='*60}")
    print(f"✅ Combined file saved → {filename} ({len(combined_df)} total games)")
    
    return combined_df


def scrape_multiple_dates(dates_list, output_filename="NBA_all_games.xlsx", save_individual=False):
    """
    Scrape multiple specific dates and combine into one file.
    
    Args:
        dates_list: List of date strings in format YYYY-MM-DD
        output_filename: Name of the output Excel file
        save_individual: If True, also save individual files for each date
        
    Returns:
        Combined DataFrame with all games
    """
    all_games = []
    
    print(f"\n📅 Scraping {len(dates_list)} dates...\n")
    
    for date_str in dates_list:
        try:
            df = scrape_donbest(date_str, save_file=save_individual)
            if not df.empty:
                all_games.append(df)
        except Exception as e:
            print(f"❌ Error scraping {date_str}: {e}")
    
    if not all_games:
        print("\n❌ No games found")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_games, ignore_index=True)
    combined_df.to_excel(output_filename, index=False)
    print(f"\n{'='*60}")
    print(f"✅ Combined file saved → {output_filename} ({len(combined_df)} total games)")
    
    return combined_df


if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv or "-d" in sys.argv
    combine_only = "--combine" in sys.argv or "-c" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ["--debug", "-d", "--combine", "-c"]]
    
    if len(args) == 1:
        # Command line usage: python scraper.py YYYY-MM-DD [--debug]
        date = args[0]
        scrape_donbest(date, debug=debug_mode)
    elif len(args) == 2:
        # Command line usage: python scraper.py YYYY-MM-DD YYYY-MM-DD [--debug] [--combine]
        start_date = args[0]
        end_date = args[1]
        scrape_date_range(start_date, end_date, combine_only=combine_only)
    else:
        # Example usage
        print("Usage examples:")
        print("  python scraper.py 2025-10-31")
        print("  python scraper.py 2025-10-31 --debug  (for debugging)")
        print("  python scraper.py 2025-10-01 2025-10-31")
        print("  python scraper.py 2025-10-01 2025-10-31 --combine  (only combined file)")
        print("\nRunning example for 2025-10-31...\n")
        scrape_donbest("2025-10-31", debug=debug_mode)
