#!/usr/bin/env python3
# app.py

# pip install requests beautifulsoup4 openai python-dotenv
import os
import pickle

from get_docs import fetch_docs
from create_embeddings import compute_hash, get_embedding, safe_filename

# Directory to store per-doc embedding pickles
EMBEDDING_DIR = 'embeddings'
os.makedirs(EMBEDDING_DIR, exist_ok=True)


def push_to_vector_db(record):
    """Placeholder for future vector DB integration."""
    # TODO: implement code to push `record` to your vector database
    pass


def process_docs():
    docs = fetch_docs()
    # Exclude older release-notes versions, keep only the latest
    release_notes = [d for d in docs if 'release-notes' in d.get('location', '')]
    other_docs = [d for d in docs if 'release-notes' not in d.get('location', '')]
    if release_notes:
        def _ver_tuple(d):
            # parse version from title like 'n8n@1.53.2'
            parts = d.get('title', '').split('@')[-1].split('.')
            return tuple(int(p) for p in parts if p.isdigit() or p.isnumeric())
        latest = max(release_notes, key=_ver_tuple)
        docs_to_process = other_docs + [latest]
    else:
        docs_to_process = docs
    for doc in docs_to_process:
        title = doc['title']
        location = doc['location']
        text = doc['text']
        content_hash = compute_hash(text)

        filename = safe_filename(location)
        filepath = os.path.join(EMBEDDING_DIR, filename)

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                saved = pickle.load(f)
            if saved.get('content_hash') == content_hash:
                print(f"No change for '{title}'")
                continue
            print(f"Updating embedding for '{title}'")
        else:
            print(f"Creating embedding for new doc '{title}'")

        embedding = get_embedding(text)
        record = {
            'title': title,
            'location': location,
            'content_hash': content_hash,
            'embedding': embedding
        }

        with open(filepath, 'wb') as f:
            pickle.dump(record, f)
        print(f"Saved embedding to {filepath}")

        # Hook: push to vector DB
        push_to_vector_db(record)


def main():
    process_docs()
    print("All documents processed.")


if __name__ == '__main__':
    main() 