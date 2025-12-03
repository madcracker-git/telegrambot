import requests
from bs4 import BeautifulSoup

# Check Game 545 and 546: SAS @ NOP on 10/24
r = requests.get('http://server1.donbest.com/scores/2025-10-24/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

in_nba = False
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 10:
        continue
    
    cell_texts = [cell.get_text(strip=True) for cell in cells]
    full_text = ' '.join(cell_texts).upper()
    
    if 'NBA' in full_text and ('FRIDAY' in full_text or 'THURSDAY' in full_text):
        in_nba = True
        continue
    
    if in_nba:
        if 'COLLEGE' in full_text or 'NCAA' in full_text:
            in_nba = False
            continue
        
        if len(cell_texts) > 1 and cell_texts[0] in ['545', '546']:
            print(f"Game {cell_texts[0]}: {cell_texts[1]}")
            print(f"  All cells: {cell_texts[:15]}")
            print()

