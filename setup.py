import pickle
from rag import *

chunks = []
with open("data.md", "r") as file:
    documentation = file.read()
    chunks = parse_markdown_by_levels(documentation)

with open("./data.pickle", "wb") as file:
    pickle.dump(chunks, file)

insert_chunks_to_pinecone(chunks)
