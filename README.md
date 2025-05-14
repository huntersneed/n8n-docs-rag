# n8n Docs RAG Embeddings

This repository demonstrates a simple pipeline to fetch HTML-based documentation from n8n, clean and extract text, generate embeddings using OpenAI, and store them for use in a Retrieval-Augmented Generation (RAG) or vector database system.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Scripts](#scripts)
  - [`get_docs.py`](#get_docspy)
  - [`create_embeddings.py`](#create_embeddingspyy)
  - [`app.py`](#apppy)
- [How It Works](#how-it-works)
- [Usage Examples](#usage-examples)
- [Next Steps](#next-steps)
- [License](#license)

## Overview

1. **Fetch and clean**: Pull the latest docs index (`search_index.json`) from n8n's site, strip out HTML tags, and store plain text.  
2. **Compute embeddings**: Use OpenAI's Embedding API to turn each document into a fixed-size vector.  
3. **Change detection**: Track document content via a SHA-256 hash to only update embeddings when content changes.  
4. **Orchestration**: `app.py` ties everything together and provides a hook for pushing into a vector database.

## Directory Structure

```text
├── get_docs.py           # Module to fetch & clean docs
├── create_embeddings.py  # Compute & store per-doc embeddings
├── app.py                # Orchestrator script
├── embeddings/           # Auto-generated pickle files
├── README.md             # Project overview & instructions
├── .env                  # (Optional) environment variables
```

### Pickle (.pkl) Files

`pickle` is a Python standard library for serializing and deserializing objects to and from files. In this project, each document's metadata and embedding vector is stored in the `embeddings/` directory as a `.pkl` file. Each file contains a Python dictionary with:

- `title`: Document title
- `location`: Document path or URL fragment
- `content_hash`: SHA-256 hash of the cleaned text (used for change detection)
- `embedding`: List of floating-point numbers representing the embedding vector

You can load and inspect a pickle file with:

```python
import pickle

with open('embeddings/example_doc.pkl', 'rb') as f:
    record = pickle.load(f)
print(record)
```

## Prerequisites

- Python 3.7+  
- An OpenAI API key  

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/n8n-docs-rag.git
   cd n8n-docs-rag
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install requests beautifulsoup4 openai python-dotenv
   ```

## Environment Variables

Create a `.env` file in the project root with your OpenAI API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

## Scripts

### `get_docs.py`

- Fetches `search_index.json` from `https://docs.n8n.io` (with optional cookies).  
- Parses each document's HTML and returns a list of dicts with `title`, `location`, and cleaned `text` via `fetch_docs()`.

### `create_embeddings.py`

- Imports `fetch_docs()` for plain text docs.  
- Computes a SHA-256 hash of each document's text.  
- Calls OpenAI's Embedding API (default `text-embedding-3-small`, adjustable) to generate a vector.  
- Saves or updates a pickle (`.pkl`) per doc in `embeddings/`, including title, location, hash, and embedding.

### `app.py`

- High-level orchestrator.  
- Loops through cleaned docs, generates or updates embeddings, and writes them to disk.  
- Includes a stub `push_to_vector_db(record)` for future vector database integration.

## How It Works

1. **Fetch & Clean**: `get_docs.fetch_docs()` retrieves the JSON index and uses BeautifulSoup to strip HTML.  
2. **Hash**: A SHA-256 hash of the cleaned text identifies changes.  
3. **Embedding**: If content is new or changed, call OpenAI's embedding endpoint.  
4. **Persistent Storage**: Pickle files hold the embedding + metadata.  
5. **Orchestration**: `app.py` ties everything together and prints status.

## Usage Examples

1. Fetch and view docs:
   ```bash
   python get_docs.py
   ```
2. Generate or update embeddings for all docs:
   ```bash
   python create_embeddings.py
   ```
3. Full pipeline:
   ```bash
   python app.py
   ```

## Next Steps

- Implement `push_to_vector_db(record)` in `app.py` to insert/update vectors in a vector database (e.g., Pinecone, Weaviate).  
- Add batching or chunking for very long documents.  
- Add logging, error handling, retries.  
- Build a RAG-enabled QA or chatbot interface on top of the stored vectors.

## License

This project is licensed under the MIT License. Feel free to use and adapt!