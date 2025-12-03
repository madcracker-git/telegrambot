import requests
from bs4 import BeautifulSoup

r = requests.get('http://server1.donbest.com/scores/2025-10-24/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

# Find NBA section and get actual game rows
in_nba = False
game_rows = []

for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    
    cell_texts = [cell.get_text(strip=True) for cell in cells]
    full_text = ' '.join(cell_texts).upper()
    
    if 'NBA' in full_text and ('FRIDAY' in full_text or 'THURSDAY' in full_text):
        in_nba = True
        continue
    
    if in_nba:
        # Check if this is a header row (has "1H" and "2H" as text, not numbers)
        if len(cell_texts) > 8 and ('1H' in cell_texts[7] or '2H' in cell_texts[8]):
            print("Header row found:")
            for i, text in enumerate(cell_texts[:12]):
                print(f"  {i}: '{text}'")
            continue
        
        # Check if this is a game row (starts with game ID)
        if cell_texts[0].isdigit() and len(cell_texts[0]) >= 3:
            if '540' in cell_texts[0] or '541' in cell_texts[0]:
                print(f"\nGame row {cell_texts[0]}:")
                print(f"  Total cells: {len(cells)}")
                for i, text in enumerate(cell_texts[:12]):
                    print(f"  Cell {i}: '{text}'")
                game_rows.append((cell_texts[0], cell_texts))
                if len(game_rows) >= 2:
                    break

