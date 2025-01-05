import re
from pinecone import Pinecone
from typing import List, Dict
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")

openai.api_key=OPENAI_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("crustdata")

def parse_markdown_by_levels(documentation: str) -> List[Dict]:
    """
    Parse markdown content by level and store chunks with metadata.
    """
    chunks = []
    current_chunk = {"tags": [], "content": ""}
    tags = []
    level_pattern = re.compile(r"^(#{2,6})\s+(.*)")

    for line in documentation.splitlines():
        match = level_pattern.match(line)
        if match:
            # Identify the level of the header and content
            level, header = len(match.group(1)), match.group(2).strip()

            # If the level is within top 3, update tags
            if level <= 3:
                if len(tags) < level:
                    tags = tags[:level - 1] + [header]
                else:
                    tags[level - 1] = header

            # Store the current chunk and reset
            if current_chunk["content"]:
                chunks.append(current_chunk)
                current_chunk = {"tags": tags[:3], "content": ""}

        # Append content to the current chunk
        current_chunk["content"] += line + "\n"

    # Add the last chunk
    if current_chunk["content"]:
        chunks.append(current_chunk)

    return chunks

def insert_chunks_to_pinecone(chunks: List[Dict]):
    """
    Insert chunk and its metadata into Pinecone.
    """
    for idx, chunk in enumerate(chunks):
        # Generate embedding
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["content"],
        )

        embedding = response.data[0].embedding

        # Metadata
        metadata = {
            "tags": chunk["tags"],
            "index": idx,
        }

        # Upsert into Pinecone
        index.upsert([(str(idx), embedding, metadata)], namespace="")

def search_top_k(query: str, top_k: int = 3) -> List[Dict]:
    """
    Generate vector embedding for a query and fetch top-K results from Pinecone.
    """
    try:
        # Generate query embedding
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_embedding = response.data[0].embedding

        # Query Pinecone for top-K results
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            include_values=False  # Only return metadata and scores
        )

        # Extract and return results
        return [
            {
                "id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            }
            for match in results["matches"]
        ]
    except Exception as e:
        print(f"An error occurred during search: {e}")
        return []
    
def get_chunks_by_index(indices: List[int], chunks: List[Dict]) -> List[str]:
    """
    Fetch the content of chunks by their indices.
    """
    return [
        chunks[int(i)]["content"] for i in indices
    ]