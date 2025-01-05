# Crustdata

Crustdata is a platform that provides programmatic access to firmographic and growth metrics data for companies worldwide. This repository offers an interface to query Crustdata API documentation efficiently using a vector-based search powered by Pinecone.

The project is designed to allow users to query and retrieve relevant information from the documentation, which is chunked, indexed, and stored in a vector database for fast and effective retrieval.

---

## Features

- **Documentation Parsing**: Automatically parses Markdown documentation into chunks.
- **Embeddings**: Creates embeddings of parsed chunks using OpenAI's API.
- **Pinecone Integration**: Stores the embeddings in a Pinecone vector database for fast retrieval.
- **Search Interface**: Streamlit application for querying the API documentation via a conversational interface.

---

## Setup

Initial Setup

Step 1: Run setup.py to Create Embeddings and Store Them in Vector Database

To generate embeddings for the documentation and store them in the Pinecone vector database, run the following command:

```bash
python setup.py
```

This will:
	•	Parse the content of Data.md.
	•	Generate embeddings for each chunk of documentation using OpenAI’s API.
	•	Store the embeddings in the Pinecone vector database.
	•	Serialize the indexed chunks and save them as Data.pickle.

Step 2: Run the Streamlit Application

Once the embeddings are generated and indexed, you can start the Streamlit web application, which serves as the interface for querying the documentation.

```bash
streamlit run app.py
```

This will open a browser window with a search box where you can input queries. The app will process the query, retrieve the most relevant documentation, and display the results.
