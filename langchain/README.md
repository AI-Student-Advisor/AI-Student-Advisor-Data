# Data Loading

This directory contains the code to load the data into the Pinecone vector store.

## Setup

1. Create python virtual environment.

```bash
python3 -m venv .venv
```

2. Activate the virtual environment.

```bash
source .venv/bin/activate
```

3. Install the required packages.

```bash
pip install -r requirements.txt
```

4. Run the script to load the data into the Pinecone vector store.

```bash
python data_loader.py
```

## Bug

Need to make a change to the package `langchain_pinecone` due to a bug because of which its unable to find the API key required for Pinecone.

This is a temporary fix and will be removed once the bug is fixed.

The code file to be edited should be present at (from root): `langchain/.venv/lib/python3.12/site-packages/langchain_pinecone/vectorstores.py`.

You will need to edit the `_pinecone_api_key` variable in the `get_pinecone_index` function. Set this variable to your Pinecone API key.
