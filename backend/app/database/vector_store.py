# import os
# import chromadb
# from chromadb.utils import embedding_functions
# from app.config import settings

# def get_chroma_client():
#     # Store ChromaDB locally in root of backend directory
#     persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
#     return chromadb.PersistentClient(path=persist_dir)

# def initialize_rag():
#     try:
#         client = get_chroma_client()
        
#         # Use sentence-transformers for local, fast, offline embeddings
#         embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
#         collection = client.get_or_create_collection(
#             name="lesson_chunks",
#             embedding_function=embedding_fn
#         )
#         return collection
#     except Exception as e:
#         print(f"Failed to initialize ChromaDB collection: {e}")
#         raise e

import os
import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

def get_chroma_client():
    persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
    return chromadb.PersistentClient(path=persist_dir)

def initialize_rag():
    try:
        client = get_chroma_client()
        
        # Use local reliable embedding (recommended for stability)
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        collection = client.get_or_create_collection(
            name="lesson_chunks",
            embedding_function=embedding_fn
        )
        print("✅ ChromaDB initialized with local embeddings (all-MiniLM-L6-v2)")
        return collection
    except Exception as e:
        print(f"❌ Failed to initialize ChromaDB: {e}")
        raise e