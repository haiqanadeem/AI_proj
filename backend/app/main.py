from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, lessons, voice, tutor, quiz, code, progress
from app.database.connection import init_db, SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    print("Starting up CodeSight AI Backend...")
    # Initialize SQL database tables
    init_db()
    print("Database tables created/verified.")

    # Auto-seed lessons + ChromaDB if database is empty
    try:
        from app.database.seed import seed_db
        db = SessionLocal()
        try:
            seed_db(db)
        finally:
            db.close()
    except Exception as e:
        print(f"Warning: Auto-seed encountered an issue: {e}")

    yield
    print("Shutting down CodeSight AI Backend...")


app = FastAPI(
    title="CodeSight AI API",
    description="Voice-First Programming Learning Platform for Visually Impaired Students Backend API",
    version="1.0",
    lifespan=lifespan,
)

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


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "CodeSight AI API Server",
        "version": "1.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint per roadmap Phase 0 milestone."""
    return {"status": "ok"}
