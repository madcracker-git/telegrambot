import requests
from bs4 import BeautifulSoup

r = requests.get('http://server1.donbest.com/scores/2025-10-23/all.html')
soup = BeautifulSoup(r.text, 'html.parser')

for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) < 2:
        continue
    
    game_id = cells[0].get_text(strip=True)
    team = cells[1].get_text(strip=True)
    
    if game_id in ['531', '532']:
        print(f"Game {game_id}: {team}")

