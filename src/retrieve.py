# Phase 1: Your job is to implement retrieve() below.

from db import get_collection


def retrieve(query: str, n: int = 3) -> list[dict]:
    """
    Return the top-n most relevant chunks from ChromaDB for the given query.
    Each result should be a dict with at least: {"text": str, "book": int}
    """
    raise NotImplementedError("Write this yourself — see Phase 1 in the prospectus")
