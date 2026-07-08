# Scope: Backend (Milestones 1+2)

## Architecture
Three-layer backend: FastAPI API routers → AI/Service modules → SQLAlchemy models + PostgreSQL/ChromaDB

## Sub-Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| A | Foundation & Infrastructure | docker-compose.yml, .env, requirements.txt, config.py, all 8 SQLAlchemy models, database connection, seed data (15+ lessons), ChromaDB vector store init | none | PLANNED |
| B | AI Modules & Services | All 7 AI modules (tutor_chain, rag_retriever, intent_classifier, quiz_generator, code_analyzer, adaptive_engine, progress_predictor) + auth_service + code_sandbox | A | PLANNED |
| C | API Layer & Integration | All 7 API routers (auth, lessons, quiz, voice, code, tutor, progress) + main.py + utils (security, validators) | A, B | PLANNED |

## Interface Contracts
### Sub-milestone A → B
- Models importable from app.models.*
- Database session via app.database.connection.get_db()
- ChromaDB collection via app.database.vector_store

### Sub-milestone B → C  
- AI modules callable from app.ai.*
- Services callable from app.services.*
- All return structured dicts matching API spec

### Sub-milestone A → C
- Models used directly in API routers for CRUD operations

## Key Constraint
Use Google Gemini (gemini-2.0-flash) for ALL AI modules, NOT OpenAI GPT-4o.
Use sentence-transformers or Gemini embeddings for ChromaDB (not OpenAI embeddings).
