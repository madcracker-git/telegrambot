"""
Check 2H results for specific games from the user's list
"""

import pandas as pd
import re

# Read the combined Excel file
df = pd.read_excel("NBA_all_games.xlsx")

# Games to check (from user's list)
games_to_check = [
    ("2025-10-23", 532, "DEN", "GSW"),
    ("2025-10-24", 540, "MIL", "TOR"),
    ("2025-10-24", 538, "BOS", "NYK"),
    ("2025-10-24", 546, "SAS", "NOP"),
    ("2025-10-27", 524, "ATL", "CHI"),
    ("2025-10-27", 529, "TOR", "SAS"),
    ("2025-10-29", 552, "ORL", "DET"),
    ("2025-10-29", 564, "POR", "UTA"),
    ("2025-10-29", 568, "LAL", "MIN"),
    ("2025-10-29", 570, "MEM", "PHX"),
    ("2025-10-31", 510, "ATL", "IND"),
    ("2025-10-31", 514, "TOR", "CLE"),
    ("2025-10-31", 523, "NOP", "LAC"),
    ("2025-11-01", 528, "MIN", "CHA"),
    ("2025-11-01", 529, "ORL", "WAS"),
    ("2025-11-02", 546, "MEM", "TOR"),
    ("2025-11-02", 543, "UTA", "CHA"),
    ("2025-11-03", 558, "WAS", "NYK"),
    ("2025-11-03", 568, "LAL", "POR"),
    ("2025-11-03", 0, "MIA", "LAC"),  # Game ID 0
    ("2025-11-05", 516, "BKN", "IND"),
    ("2025-11-07", 542, "TOR", "ATL"),
    ("2025-11-07", 549, "UTA", "MIN"),
    ("2025-11-08", 569, "NOP", "SAS"),
    ("2025-11-09", 506, "OKC", "MEM"),
    ("2025-11-09", 508, "BOS", "ORL"),
    ("2025-11-10", 532, "ATL", "LAC"),
    ("2025-11-11", 544, "DEN", "SAC"),
    ("2025-11-12", 551, "CLE", "MIA"),
    ("2025-11-12", 560, "POR", "NOP"),
    ("2025-11-14", 518, "GSW", "SAS"),
    ("2025-11-15", 526, "LAL", "MIL"),
    ("2025-11-15", 528, "DEN", "MIN"),
    ("2025-11-16", 534, "BKN", "WAS"),
    ("2025-11-16", 538, "ORL", "HOU"),
    ("2025-11-17", 552, "NYK", "MIA"),
    ("2025-11-17", 555, "OKC", "NOP"),
    ("2025-11-18", 566, "MEM", "SAS"),
    ("2025-11-18", 569, "UTA", "LAL"),
    ("2025-11-19", 516, "NYK", "DAL"),
    ("2025-11-20", 526, "PHI", "MIL"),
    ("2025-11-21", 530, "WAS", "TOR"),
    ("2025-11-21", 540, "DEN", "HOU"),
    ("2025-11-22", 556, "MEM", "DAL"),
    ("2025-11-23", 572, "LAL", "UTA"),
    ("2025-11-24", 508, "NYK", "BKN"),
    ("2025-11-26", 532, "IND", "TOR"),
    ("2025-11-26", 528, "DET", "BOS"),
    ("2025-11-26", 534, "MIN", "OKC"),
    ("2025-11-26", 542, "SAS", "POR"),
    ("2025-11-26", 544, "PHX", "SAC"),
    ("2025-11-28", 550, "WAS", "IND"),
    ("2025-11-28", 562, "SAC", "UTA"),
    ("2025-11-29", 502, "BOS", "MIN"),
    ("2025-11-29", 514, "DEN", "PHX"),
    ("2025-11-30", 517, "HOU", "UTA"),
    ("2025-11-30", 522, "BOS", "CLE"),
    ("2025-11-30", 531, "NOP", "LAL"),
    ("2025-12-01", 538, "ATL", "DET"),
    ("2025-12-01", 541, "LAC", "MIA"),
]

print("=" * 80)
print("2H RESULTS FOR SPECIFIC GAMES")
print("=" * 80)
print()

results_found = []
results_not_found = []

for date, game_id, team1, team2 in games_to_check:
    # Try to find the game
    # Match by date and teams (either order)
    matches = df[
        (df["Date"] == date) & 
        (
            ((df["Away Team"] == team1) & (df["Home Team"] == team2)) |
            ((df["Away Team"] == team2) & (df["Home Team"] == team1))
        )
    ]
    
    if len(matches) > 0:
        game = matches.iloc[0]
        away_team = game["Away Team"]
        home_team = game["Home Team"]
        away_2h = game["2H Away"]
        home_2h = game["2H Home"]
        total_2h = game["2H Total"]
        
        results_found.append({
            "date": date,
            "game_id": game_id,
            "away": away_team,
            "home": home_team,
            "away_2h": away_2h,
            "home_2h": home_2h,
            "total_2h": total_2h
        })
        
        print(f"{date} | Game {game_id}: {away_team} @ {home_team}")
        print(f"  2H: {away_team} {away_2h} - {home_team} {home_2h} | Total: {total_2h}")
        print()
    else:
        results_not_found.append((date, game_id, team1, team2))
        print(f"{date} | Game {game_id}: {team1} @ {team2} - NOT FOUND")
        print()

print("=" * 80)
print(f"Found: {len(results_found)} games")
print(f"Not Found: {len(results_not_found)} games")
print("=" * 80)

# Save results to CSV
if results_found:
    results_df = pd.DataFrame(results_found)
    results_df.to_excel("2H_results_specific_games.xlsx", index=False)
    print("\n✅ Results saved to: 2H_results_specific_games.xlsx")

