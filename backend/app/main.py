from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api import auth, lessons, voice, tutor, quiz, code, progress, voice_logs
from app.database.connection import init_db, SessionLocal, get_db
from app.database.vector_store import get_chroma_client
from app.config import settings

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    print("Starting up CodeSight AI Backend...")
    init_db()
    print("Database tables created/verified.")

    try:
        from app.database.seed import seed_db
        db = SessionLocal()
        try:
            seed_db(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Warning: Auto-seed encountered an issue: {e}")

    # Pre-pull Docker image for sandbox execution
    try:
        import docker
        print("Pre-pulling sandbox Docker image (python:3.11-slim) in background...")
        client = docker.from_env()
        client.images.pull("python:3.11-slim")
        print("Sandbox Docker image is ready.")
    except Exception as e:
        print(f"Warning: Could not pre-pull Docker image: {e}")

    yield
    print("Shutting down CodeSight AI Backend...")

app = FastAPI(
    title="CodeSight AI API",
    description="Voice-First Programming Learning Platform for Visually Impaired Students Backend API",
    version="1.0",
    lifespan=lifespan,
)

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(voice.router)
app.include_router(tutor.router)
app.include_router(quiz.router)
app.include_router(code.router)
app.include_router(progress.router)
app.include_router(voice_logs.router)

@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {
        "status": "healthy",
        "service": "CodeSight AI API Server",
        "version": "1.0"
    }

@app.get("/health")
@limiter.limit("5/minute")
def health_check(request: Request, db: Session = Depends(get_db)):
    """Comprehensive health check endpoint (DB, ChromaDB, Gemini)."""
    health_status = {"status": "ok", "db": "unknown", "chroma": "unknown", "gemini": "unknown"}
    
    # 1. DB Check
    try:
        db.execute(text("SELECT 1"))
        health_status["db"] = "ok"
    except Exception as e:
        health_status["db"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
        
    # 2. ChromaDB Check
    try:
        client = get_chroma_client()
        client.heartbeat()
        health_status["chroma"] = "ok"
    except Exception as e:
        health_status["chroma"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
        
    # 3. Gemini Check (using simple connection check)
    try:
        if not settings.GOOGLE_API_KEY:
            health_status["gemini"] = "error: GOOGLE_API_KEY not set"
            health_status["status"] = "degraded"
        else:
            # For a fast health check, we could just rely on the API key presence,
            # but an actual API call is requested. We use a tiny prompt to minimize latency/cost.
            from app.ai.gemini_client import call_gemini
            # Just test connectivity and authentication without actually generating a long response
            call_gemini("ping", expect_json=False)
            health_status["gemini"] = "ok"
    except Exception as e:
        health_status["gemini"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
        
    return health_status
