# Phase 1: Your job is to implement chunk_text() and embed_and_store() below.
# The db.get_collection() boilerplate is provided — the rest is yours.

from db import get_collection
import re
from sentence_transformers import SentenceTransformer
import chromadb
import uuid

def chunk_text(text: str) -> list[dict]:
    """
    Split text into chunks by book/canto boundaries.
    Each chunk should be ~300-500 words and include metadata:
      {"text": str, "book": int, "line_start": int, "line_end": int}
    """

    # books = re.split(r'Book \w+\n',text)[1:] #For Paradise Lost
    # book_objects = []
    # for index in range(len(books)):

    #     lines = books[index].split('\n')
    #     lines = [line.replace('    ','\t') for line in lines if line]

    #     books[index] = '\n'.join(lines)
    #     linecount = len(lines)
    #     paragraphs = books[index].split('\t')
    #     paragraph_count = len(paragraphs)

    #     book_dict = {
    #         "book":index+1,
    #         "lineCount": linecount,
    #         "paragraphCount": paragraph_count,
    #         "paragraphs": paragraphs
    #     }

    #     book_objects.append(book_dict)

    #     chunks = []

    # for book_object in book_objects:
    #     for paragraph in book_object['paragraphs']:
    #         chunks.append({
    #             "book":book_object['book'],
    #             "text":paragraph
    #         })
    
    # return chunks

    books = re.split(r'BOOK \w+\.\n',text) #For Iliad
    books[len(books)-1] = books[len(books)-1].split("CONCLUDING NOTE")[0]
    books = [book for book in books if book.strip()][2:]

    book_objects = []
    for index in range(len(books)):

        #lines = books[index].split('\n')
        #lines = [line.strip() for line in lines if line]

        #books[index] = '\n'.join(lines)
        #linecount = len(lines)
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
    
    chunks = [chunk for chunk in chunks if 'Illustration' not in chunk['text']]

    return chunks

    

def embed_and_store(chunks: list[dict]) -> None:
    """
    Embed each chunk using sentence-transformers and store in ChromaDB.
    Use model: all-MiniLM-L6-v2
    """
    collection: chromadb.Collection = get_collection('socratic_engine')
    transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    #for chunk in chunks:
        #chunk['embedding'] = transformer.encode(chunk['text'])

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
