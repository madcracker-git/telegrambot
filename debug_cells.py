import requests
from bs4 import BeautifulSoup

r = requests.get('http://server1.donbest.com/scores/2025-10-24/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

# Find NBA section
in_nba = False
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    
    cell_texts = [cell.get_text(strip=True) for cell in cells]
    full_text = ' '.join(cell_texts).upper()
    
    if 'NBA' in full_text and ('FRIDAY' in full_text or 'THURSDAY' in full_text):
        in_nba = True
        continue
    
    if in_nba and '540' in cell_texts[0]:
        print("Found Game 540:")
        print(f"Total cells: {len(cells)}")
        for i, text in enumerate(cell_texts[:15]):
            print(f"  Cell {i}: '{text}'")
        
        # Also check next row (should be TOR)
        next_row = row.find_next_sibling('tr')
        if next_row:
            next_cells = next_row.find_all('td')
            next_texts = [cell.get_text(strip=True) for cell in next_cells]
            if '541' in next_texts[0] or 'TOR' in ' '.join(next_texts):
                print("\nNext row (should be TOR):")
                for i, text in enumerate(next_texts[:15]):
                    print(f"  Cell {i}: '{text}'")
        break

