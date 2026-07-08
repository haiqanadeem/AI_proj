import os
import chromadb
from app.config import settings

import urllib.request
import json

class GoogleGeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        if self.api_key:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        if not self.api_key:
            # Fallback mock embeddings for testing offline
            return [[0.1] * 768 for _ in input]
        try:
            import google.generativeai as genai
            response = genai.embed_content(
                model="models/gemini-embedding-001",
                content=input,
                task_type="retrieval_document"
            )
            return response['embedding']
        except Exception as e:
            print(f"Embedding error: {e}. Falling back to mock embeddings.")
            return [[0.1] * 768 for _ in input]

def get_chroma_client():
    # Store ChromaDB locally in root of backend directory
    persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
    return chromadb.PersistentClient(path=persist_dir)

def initialize_rag():
    client = get_chroma_client()
    embedding_fn = GoogleGeminiEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="lesson_chunks",
        embedding_function=embedding_fn
    )
    return collection
