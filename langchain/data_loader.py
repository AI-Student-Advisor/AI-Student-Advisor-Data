"""
Data Loader

This module is responsible for loading the data from the data source to the vector store. 

This also involves:
1. Loading the data from source.
2. Transform the data so embeddings can be generated.
    a. Chunk the data into smaller pieces.
3. Generate embeddings for the data.
4. Store the embeddings in the vector store.
"""
from dotenv import dotenv_values
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# import API keys
config = dotenv_values(".env")

# index name and the data files to load
index_data = {
    "uottawa-index": "../uottawa/data/uottawa_data.jsonl"
}
# embeddings model to use
embeddings = OpenAIEmbeddings(
    openai_api_key=config["OPENAI_API_KEY"],
    model="text-embedding-3-small",
    dimensions=1536
    )

# function to extract metadata from each record
def metadata_func(record: dict, metadata: dict) -> dict:
    # set source
    metadata["source"] = record.get("source")
    # copy all elements from metadata field in record to metadata
    metadata.update(record.get("metadata", {}))
    return metadata

def main():
    # for each data file
    for index_name, data_file in index_data.items():
        # setup loader
        loader = JSONLoader(
            file_path=data_file,
            jq_schema='.',
            content_key='text',
            json_lines=True,
            metadata_func=metadata_func
        )

        # load the documents
        docs = loader.load()

        # Generate embeddings, create index and save to the vector store
        PineconeVectorStore.from_documents(
            docs,
            embeddings,
            index_name=index_name
        )

if __name__ == "__main__":
    main()