import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.ai.intent_classifier import call_ollama, classify_voice_intent
from app.database.vector_store import initialize_rag

def test_ollama():
    print("Testing call_ollama (json format)...")
    res = call_ollama("Respond with {\"test\": \"success\"} exactly.")
    print("Result:", res)

    print("\nTesting intent classification...")
    intent = classify_voice_intent("open the python variables lesson")
    print("Intent:", intent)

def test_rag():
    print("\nTesting RAG initialization and embedding fallback...")
    try:
        collection = initialize_rag()
        print("Collection retrieved:", collection.name)
        
        # Test an embedding query
        results = collection.query(
            query_texts=["variables"],
            n_results=1
        )
        print("RAG Query Results:", results)
    except Exception as e:
        print("RAG Error:", e)

if __name__ == "__main__":
    test_ollama()
    test_rag()
