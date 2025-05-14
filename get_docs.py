import requests
import json
from bs4 import BeautifulSoup

def fetch_docs():
    resp = requests.get('https://docs.n8n.io/search/search_index.json')
    resp.raise_for_status()
    data = resp.json()
    docs = []
    for doc in data.get('docs', []):
        title = doc.get('title')
        location = doc.get('location')
        raw_html = doc.get('text', '')
        soup = BeautifulSoup(raw_html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        docs.append({'title': title, 'location': location, 'text': text})
    return docs

if __name__ == '__main__':
    for doc in fetch_docs():
        print(doc['title'])
        print(doc['location'])
        print(doc['text'])
        print('--------------------------------')
        print()

