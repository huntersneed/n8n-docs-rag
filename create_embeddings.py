#!/usr/bin/env python3
# create_embeddings.py

# pip install requests beautifulsoup4 openai python-dotenv
import os
import pickle
import hashlib
from get_docs import fetch_docs
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
output_dir = 'embeddings'
os.makedirs(output_dir, exist_ok=True)


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_embedding(text: str):
    # Adjust model as needed (OpenAI v1 API)
    resp = openai.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return resp.data[0].embedding


def safe_filename(location: str) -> str:
    # Strip leading/trailing slashes and replace separators
    name = location.strip('/').replace('/', '_').replace(' ', '_')
    return f"{name}.pkl"


def main():
    for doc in fetch_docs():
        title = doc.get('title')
        location = doc.get('location')
        text = doc.get('text', '')
        content_hash = compute_hash(text)

        filename = safe_filename(location)
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                saved = pickle.load(f)
            if saved.get('content_hash') == content_hash:
                print(f"No change for '{title}'")
                continue
            else:
                print(f"Updating embedding for '{title}'")
        else:
            print(f"Creating embedding for new doc '{title}'")

        embedding = get_embedding(text)
        to_save = {
            'title': title,
            'location': location,
            'content_hash': content_hash,
            'embedding': embedding
        }
        with open(filepath, 'wb') as f:
            pickle.dump(to_save, f)
        print(f"Saved: {filepath}")


if __name__ == '__main__':
    main() 