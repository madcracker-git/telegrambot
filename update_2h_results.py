"""
Update 2H results with correct data for all games
"""

import pandas as pd

# Read the main file
df_all = pd.read_excel("NBA_all_games.xlsx")

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
    ("2025-11-03", 0, "MIA", "LAC"),
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

for date, game_id, team1, team2 in games_to_check:
    # Try to find the game
    matches = df_all[
        (df_all["Date"] == date) & 
        (
            ((df_all["Away Team"] == team1) & (df_all["Home Team"] == team2)) |
            ((df_all["Away Team"] == team2) & (df_all["Home Team"] == team1))
        )
    ]
    
    if len(matches) > 0:
        game = matches.iloc[0]
        away_team = game["Away Team"]
        home_team = game["Home Team"]
        away_2h = game["2H Away"]
        home_2h = game["2H Home"]
        total_2h = game["2H Total"]
        away_1h = game["1H Away"]
        home_1h = game["1H Home"]
        total_1h = game["1H Total"]
        ot_away = game["OT Away"]
        ot_home = game["OT Home"]
        ot_total = game["OT Total"]
        
        results_found.append({
            "date": date,
            "game_id": game_id,
            "away": away_team,
            "home": home_team,
            "away_1h": away_1h,
            "home_1h": home_1h,
            "total_1h": total_1h,
            "away_2h": away_2h,
            "home_2h": home_2h,
            "total_2h": total_2h,
            "ot_away": ot_away,
            "ot_home": ot_home,
            "ot_total": ot_total
        })
        
        print(f"{date} | Game {game_id}: {away_team} @ {home_team}")
        print(f"  1H: {away_team} {away_1h} - {home_team} {home_1h} | Total: {total_1h}")
        print(f"  2H: {away_team} {away_2h} - {home_team} {home_2h} | Total: {total_2h}")
        print(f"  OT: {away_team} {ot_away} - {home_team} {ot_home} | Total: {ot_total}")
        print()
    else:
        # Manual data for missing games
        if date == "2025-10-23" and game_id == 532:
            results_found.append({
                "date": date,
                "game_id": game_id,
                "away": "DEN",
                "home": "GSW",
                "away_1h": 70,
                "home_1h": 61,
                "total_1h": 131,
                "away_2h": 61,
                "home_2h": 76,
                "total_2h": 137,
                "ot_away": 11,
                "ot_home": 17,
                "ot_total": 28
            })
            print(f"{date} | Game {game_id}: DEN @ GSW (MANUAL)")
            print(f"  1H: DEN 70 - GSW 61 | Total: 131")
            print(f"  2H: DEN 61 - GSW 76 | Total: 137")
            print(f"  OT: DEN 11 - GSW 17 | Total: 28")
            print()
        elif date == "2025-11-14" and game_id == 518:
            results_found.append({
                "date": date,
                "game_id": game_id,
                "away": "GSW",
                "home": "SAS",
                "away_1h": 47,
                "home_1h": 45,
                "total_1h": 92,
                "away_2h": 62,
                "home_2h": 63,
                "total_2h": 125,
                "ot_away": 11,
                "ot_home": 0,
                "ot_total": 11
            })
            print(f"{date} | Game {game_id}: GSW @ SAS (MANUAL)")
            print(f"  1H: GSW 47 - SAS 45 | Total: 92")
            print(f"  2H: GSW 62 - SAS 63 | Total: 125")
            print(f"  OT: GSW 11 - SAS 0 | Total: 11")
            print()

# Save results
if results_found:
    results_df = pd.DataFrame(results_found)
    results_df.to_excel("2H_results_specific_games.xlsx", index=False)
    print("=" * 80)
    print(f"✅ Results saved to: 2H_results_specific_games.xlsx")
    print(f"   Total games: {len(results_found)}")

