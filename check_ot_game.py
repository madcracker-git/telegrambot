import requests
from bs4 import BeautifulSoup

# Check Game 546: SAS @ NOP on 10/24
r = requests.get('http://server1.donbest.com/scores/2025-10-24/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 10:
        continue
    
    cell_texts = [cell.get_text(strip=True) for cell in cells]
    
    if '546' in cell_texts[0] or '547' in cell_texts[0]:
        print(f"Game {cell_texts[0]}: {cell_texts[1]}")
        print(f"  Cells: {cell_texts[:12]}")
        
        # Check for OT indicator
        if len(cell_texts) > 7:
            print(f"  Cell 7 (OT indicator): '{cell_texts[7]}'")
        
        # Parse scores
        if len(cell_texts) > 5:
            q1 = cell_texts[2] if len(cell_texts) > 2 else None
            q2 = cell_texts[3] if len(cell_texts) > 3 else None
            q3 = cell_texts[4] if len(cell_texts) > 4 else None
            q4 = cell_texts[5] if len(cell_texts) > 5 else None
            total = cell_texts[6] if len(cell_texts) > 6 else None
            ot_ind = cell_texts[7] if len(cell_texts) > 7 else None
            first_half = cell_texts[8] if len(cell_texts) > 8 else None
            second_half = cell_texts[9] if len(cell_texts) > 9 else None
            
            print(f"  Q1: {q1}, Q2: {q2}, Q3: {q3}, Q4: {q4}")
            print(f"  Total: {total}, OT Indicator: '{ot_ind}'")
            print(f"  1H: {first_half}, 2H: {second_half}")
            
            if q1 and q2 and q3 and q4:
                q_sum = int(q1) + int(q2) + int(q3) + int(q4)
                if total and total.isdigit():
                    total_int = int(total)
                    if total_int != q_sum:
                        print(f"  ⚠️  OT detected! Q sum: {q_sum}, Total: {total_int}, OT: {total_int - q_sum}")
        print()

