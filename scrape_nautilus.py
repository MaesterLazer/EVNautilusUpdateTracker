import requests, json, os
from bs4 import BeautifulSoup
from datetime import datetime

URL = 'https://nautiluslive.org/'
SELECTOR = 'h2:contains("Update") + p'  # Adjust this

def fetch():
    r = requests.get(URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    el = soup.select_one(SELECTOR)
    return el.get_text(strip=True) if el else None

def main():
    current = fetch()
    prev = open('last.txt').read().strip() if os.path.exists('last.txt') else ''
    if current and current != prev:
        with open('last.txt','w') as f: f.write(current)
        log = json.load(open('updates.json')) if os.path.exists('updates.json') else []
        log.append({'time': datetime.utcnow().isoformat(), 'text': current})
        json.dump(log, open('updates.json','w'), indent=2)

if __name__ == '__main__':
    main()
