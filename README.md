# AI Student Advisor - Data

This repository contains the code related to data preparation and loading.

For the data preparation phase, we scrap the web to get data related to the University of Ottawa and create the fine output JSON line file containing the data to be loaded into uOttawa's index in Pincone vector store.

For the data loading phase, we load the data into the Pinecone vector store by generating embeddings for the data and storing them in the Pinecone index.
