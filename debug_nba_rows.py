import requests
from bs4 import BeautifulSoup

r = requests.get('http://server1.donbest.com/scores/2025-10-23/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

# Find NBA section
in_nba = False
nba_rows_found = []

for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    
    cell_texts = [cell.get_text(strip=True) for cell in cells]
    full_text = ' '.join(cell_texts).upper()
    
    if 'NBA' in full_text and ('FRIDAY' in full_text or 'THURSDAY' in full_text):
        in_nba = True
        print("Found NBA section")
        continue
    
    if in_nba:
        # Check if we hit another sport
        if ('COLLEGE' in full_text and 'BASKETBALL' in full_text) or 'NCAA' in full_text:
            in_nba = False
            continue
        
        # Check if this is a game row
        if len(cell_texts) > 1 and cell_texts[0].isdigit():
            game_id = cell_texts[0]
            team = cell_texts[1] if len(cell_texts) > 1 else ""
            if game_id in ['531', '532'] or 'Golden' in team or 'Denver' in team:
                print(f"Found row: Game {game_id}, Team: {team}")
                nba_rows_found.append((game_id, team, cell_texts[:10]))

print(f"\nTotal NBA rows found: {len(nba_rows_found)}")
for game_id, team, cells in nba_rows_found:
    print(f"  Game {game_id}: {team} - Cells: {cells}")

