# Phase 1: Your job is to implement chunk_text() and embed_and_store() below.
# The db.get_collection() boilerplate is provided — the rest is yours.

from db import get_collection


def chunk_text(text: str) -> list[dict]:
    """
    Split text into chunks by book/canto boundaries.
    Each chunk should be ~300-500 words and include metadata:
      {"text": str, "book": int, "line_start": int, "line_end": int}
    """
    raise NotImplementedError("Write this yourself — see Phase 1 in the prospectus")


def embed_and_store(chunks: list[dict]) -> None:
    """
    Embed each chunk using sentence-transformers and store in ChromaDB.
    Use model: all-MiniLM-L6-v2
    """
    raise NotImplementedError("Write this yourself — see Phase 1 in the prospectus")


if __name__ == "__main__":
    with open("../data/texts/paradise_lost.txt", encoding="utf-8") as f:
        raw = f.read()

    chunks = chunk_text(raw)
    print(f"Created {len(chunks)} chunks")
    embed_and_store(chunks)
    print("Done — embeddings stored in ChromaDB")
