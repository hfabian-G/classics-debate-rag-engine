# Phase 1: Your job is to implement retrieve() below.

from db import get_collection
from sentence_transformers import SentenceTransformer

def retrieve(query: str, n: int = 3) -> list[dict]:
    """
    Return the top-n most relevant chunks from ChromaDB for the given query.
    Each result should be a dict with at least: {"text": str, "book": int}
    """
    collection = get_collection('socratic_engine')
    transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    t_query = transformer.encode(query)

    result = collection.query(
        query_embeddings=[t_query],
        n_results=n
    )

    chunks = []

    for i in range(n):
        chunk = {}
        chunk['text'] = result['documents'][0][i]
        chunk['book'] = result['metadatas'][0][i]['book']
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    query = 'Who is Pallas Athena'
    documents_retrieved = retrieve(query)
