import os
import sys

# Add backend app directory to sys path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.models.lesson import Lesson
from app.ai.intent_classifier import classify_voice_intent
from app.ai.rag_retriever import retrieve_context
from app.ai.quiz_generator import generate_quiz_for_topic
from app.ai.progress_predictor import predictor_model
from app.services.code_sandbox import execute_code_safely

def run_tests():
    print("=== CODESIGHT AI BACKEND INTEGRATION TESTS ===")
    
    # 1. Database Connection & Seed Data
    db = SessionLocal()
    try:
        lessons_count = db.query(Lesson).count()
        print(f"[DB Test] Seeding verification: {lessons_count} lessons found (expected: 15).")
        assert lessons_count == 15, "DB should have exactly 15 lessons."
        print("[DB Test] SUCCESS!")
    except Exception as e:
        print(f"[DB Test] FAILED: {e}")
    finally:
        db.close()
        
    # 2. Voice Intent Classifier Test
    try:
        print("\n[NLP Intent Test] Testing intent classifier for 'Open variables lesson'...")
        res = classify_voice_intent("Open variables lesson")
        print(f"[NLP Intent Test] Classified as: {res}")
        assert res.get("intent") == "OPEN_LESSON", "Expected intent to be OPEN_LESSON."
        print("[NLP Intent Test] SUCCESS!")
    except Exception as e:
        print(f"[NLP Intent Test] FAILED: {e}")
        
    # 3. RAG Retrieval Test
    try:
        print("\n[RAG Test] Testing ChromaDB document query for 'What is a variable?'...")
        context, metadata = retrieve_context("What is a variable?", difficulty="beginner", n_results=1)
        print(f"[RAG Test] Chunks retrieved: {len(metadata)}")
        print(f"[RAG Test] Chunk preview:\n{context[:150]}...")
        assert len(metadata) > 0, "RAG should return at least 1 document chunk."
        print("[RAG Test] SUCCESS!")
    except Exception as e:
        print(f"[RAG Test] FAILED: {e}")
        
    # 4. Quiz Generator Test
    try:
        print("\n[Quiz Gen Test] Testing Gemini quiz generator structure...")
        quiz = generate_quiz_for_topic("Loops", "beginner", "beginner")
        print(f"[Quiz Gen Test] Generated questions count: {len(quiz.get('questions', []))}")
        print(f"[Quiz Gen Test] First question preview: {quiz['questions'][0].get('question')}")
        assert len(quiz.get("questions", [])) == 5, "Quiz must contain exactly 5 questions."
        print("[Quiz Gen Test] SUCCESS!")
    except Exception as e:
        print(f"[Quiz Gen Test] FAILED: {e}")
        
    # 5. Sandbox Code Execution Test
    try:
        print("\n[Sandbox Test] Running code runner on clean code 'print(5 + 10)'...")
        res = execute_code_safely("print(5 + 10)")
        print(f"[Sandbox Test] Output: {res['stdout'].strip()}, exit code: {res['exit_code']}")
        assert res["stdout"].strip() == "15", "Expected output to be 15."
        assert res["exit_code"] == 0, "Expected exit code to be 0."
        print("[Sandbox Test] SUCCESS!")
    except Exception as e:
        print(f"[Sandbox Test] FAILED: {e}")

if __name__ == "__main__":
    run_tests()
