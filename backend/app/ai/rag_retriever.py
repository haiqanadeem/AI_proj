from typing import Tuple, List
from app.database.vector_store import initialize_rag

def retrieve_context(question: str, difficulty: str = None, n_results: int = 3) -> Tuple[str, List[dict]]:
    try:
        collection = initialize_rag()
        
        # Optional metadata filtering by student level/difficulty
        where_filter = {}
        if difficulty:
            where_filter["difficulty"] = difficulty
            
        results = collection.query(
            query_texts=[question],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        sources = []
        for idx, doc in enumerate(documents):
            meta = metadatas[idx] if idx < len(metadatas) else {}
            title = meta.get("lesson_title", "Unknown Lesson")
            sources.append(f"--- Context from Lesson: {title} ---\n{doc}")
            
        return "\n\n".join(sources), metadatas
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return "", []
