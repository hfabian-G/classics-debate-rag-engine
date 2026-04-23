# Phase 1: Your job is to implement chunk_text() and embed_and_store() below.
# The db.get_collection() boilerplate is provided — the rest is yours.

from db import get_collection
import re
from sentence_transformers import SentenceTransformer
import uuid

def chunk_text(text: str) -> list[dict]:
    """
    Split text into chunks by book/canto boundaries.
    Each chunk should be ~300-500 words and include metadata:
      {"text": str, "book": int, "line_start": int, "line_end": int}
    """

    books = re.split(r'BOOK \w+\.\n',text) #For Iliad
    books[len(books)-1] = books[len(books)-1].split("CONCLUDING NOTE")[0]
    books = [book for book in books if book.strip()][2:]

    book_objects = []
    for index in range(len(books)):

        paragraphs = books[index].split('\n\n')
        paragraph_count = len(paragraphs)

        book_dict = {
            "book":index+1,
            "paragraphCount": paragraph_count,
            "paragraphs": paragraphs
        }

        book_objects.append(book_dict)

    chunks = []

    for book_object in book_objects:
        for paragraph in book_object['paragraphs']:
            chunks.append({
                "id": uuid.uuid4(),
                "book":book_object['book'],
                "text":paragraph
            })
    
    chunks = [chunk for chunk in chunks if 'Illustration' not in chunk['text'] and len(chunk['text'].split(' ')) > 30]

    return chunks

def embed_and_store(chunks: list[dict]) -> None:
    """
    Embed each chunk using sentence-transformers and store in ChromaDB.
    Use model: all-MiniLM-L6-v2
    """
    collection = get_collection('socratic_engine')
    transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    chunks = [{**chunk, 'embedding': transformer.encode(chunk['text'])} for chunk in chunks]
    
    collection.add(
        ids = [str(chunk['id']) for chunk in chunks],
        documents = [chunk['text'] for chunk in chunks],
        embeddings = [chunk['embedding'] for chunk in chunks],
        metadatas = [{'book': chunk['book']} for chunk in chunks]
        )

if __name__ == "__main__":
    with open("../data/texts/the_iliad.txt", encoding="utf-8") as f:
        raw = f.read()

    chunks = chunk_text(raw)
    print(f"Created {len(chunks)} chunks")
    embed_and_store(chunks)
    print("Done — embeddings stored in ChromaDB")
