"""
Fix the missing games by manually extracting from HTML
"""

import pandas as pd

# Manual data for the missing games
missing_games = [
    {
        "Date": "2025-10-23",
        "Away Team": "DEN",
        "Home Team": "GSW",
        "1H Away": 70,
        "1H Home": 61,
        "1H Total": 131,
        "Final Away": 131,
        "Final Home": 137,
        "Final Total": 268,
        "2H Away": 61,  # Includes OT
        "2H Home": 76,  # Includes OT
        "2H Total": 137,
        "OT Away": 11,
        "OT Home": 17,
        "OT Total": 28
    },
]

# Game 518: GSW @ SAS on 11/14 (from HTML: Game 517=GSW, Game 518=SAS)
# GSW: Q1=18, Q2=29, Q3=30, Q4=32, OT=11, Total=109, 1H=47, 2H=62
# SAS: Q1=20, Q2=25, Q3=34, Q4=29, Total=108, 1H=45, 2H=63
missing_games.append({
    "Date": "2025-11-14",
    "Away Team": "GSW",
    "Home Team": "SAS",
    "1H Away": 47,
    "1H Home": 45,
    "1H Total": 92,
    "Final Away": 109,
    "Final Home": 108,
    "Final Total": 217,
    "2H Away": 62,  # Includes OT
    "2H Home": 63,
    "2H Total": 125,
    "OT Away": 11,
    "OT Home": 0,
    "OT Total": 11
})

# Read existing results
df = pd.read_excel("2H_results_specific_games.xlsx")

# Add missing games
for game in missing_games:
    df = pd.concat([df, pd.DataFrame([game])], ignore_index=True)

# Sort by date
df = df.sort_values("date").reset_index(drop=True)

# Save updated results
df.to_excel("2H_results_specific_games.xlsx", index=False)

print("✅ Updated results with missing games!")
print(f"\n10/23 Game 532: DEN @ GSW")
print(f"  2H: DEN {missing_games[0]['2H Away']} - GSW {missing_games[0]['2H Home']} | Total: {missing_games[0]['2H Total']}")

if len(missing_games) > 1:
    print(f"\n11/14 Game 518: GSW @ SAS")
    print(f"  2H: GSW {missing_games[1]['2H Away']} - SAS {missing_games[1]['2H Home']} | Total: {missing_games[1]['2H Total']}")

