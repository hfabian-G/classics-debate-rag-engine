import chromadb

def get_collection(name: str = "socratic_engine") -> chromadb.Collection:
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name)