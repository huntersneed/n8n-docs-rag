import requests
import json
from bs4 import BeautifulSoup

def fetch_docs():
    cookies = {
        'n8n_tracking_id': '3hs3ml0yu4lmamd0y16',
        '_ga': 'GA1.1.862162559.1747131569',
        '_gcl_au': '1.1.196649388.1747216050',
        '__sec__cid': '5877e26c078d640',
        '__sec__token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDczMDI1NTQsImlkIjoiNTg3N2UyNmMwNzhkNjQwIn0.qM4aJ__2G53hhV0qHpA3waJzQKADCJlX_j1GAQt4xZs',
        '__sec__fid': 'b2ebf8cf8fc59f01d82188663b090d70',
        '__sec_crid': '107d8018c85d660b4bfda4c3db5ce061ca5da15fbc92bae4e1bc10b40e608709',
        '__sec_tid': 'glrjwh',
        '_ga_0SC4FF2FH9': 'GS2.1.s1747216047$o3$g1$t1747216161$j52$l0$h0',
    }
    resp = requests.get('https://docs.n8n.io/search/search_index.json', cookies=cookies)
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

