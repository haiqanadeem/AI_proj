# System Architecture Design Document
## CodeSight AI

**Version:** 1.0  
**Date:** June 2025

---

## 1. Architecture Overview

CodeSight AI follows a **three-tier architecture** with a dedicated AI orchestration layer.

```
┌─────────────────────────────────────────────────────────────────┐
│                     TIER 1: PRESENTATION                        │
│                      Next.js 14 Frontend                        │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │ Voice Engine │  │  React UI    │  │  TTS Engine           │ │
│  │ (Whisper STT)│  │  Components  │  │  (ElevenLabs/WebSpeech│ │
│  └──────────────┘  └──────────────┘  └───────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │ REST API (HTTPS)
                              ▼
┌──────────────────────────────────
<truncated 12562 bytes>
| API authentication | JWT HS256 with 24h expiry |
| Code execution | Docker container, no network, readonly FS, 256MB RAM limit |
| API keys | Environment variables via python-dotenv |
| CORS | Whitelist only frontend origin |
| SQL injection | SQLAlchemy ORM parameterized queries |
| XSS | Next.js built-in escaping; CSP headers |

---

## 7. Deployment Architecture (Demo Setup)

```
Developer Machine
├── Docker Desktop running
│   └── PostgreSQL container
│   └── Code Sandbox containers (spun up on demand)
├── Backend: uvicorn (localhost:8000)
├── Frontend: next dev (localhost:3000)
└── ChromaDB: in-memory or local persistent
```

For production (post-demo):
- Frontend: Vercel
- Backend: Railway or Render
- Database: Supabase (PostgreSQL)
- Vector DB: ChromaDB on same server

---

## 8. Technology Stack Summary

| Layer | Technology | Version | Reason |
|---|---|---|---|
| Frontend Framework | Next.js | 14.x | SSR, routing, performance |
| UI Language | TypeScript | 5.x | Type safety, scalability |
| Styling | Tailwind CSS | 3.x | Rapid accessible UI |
| Components | ShadCN/UI | Latest | Accessible component base |
| Backend | FastAPI | 0.110+ | Python, async, AI-friendly |
| AI Orchestration | LangChain | 0.2+ | Chain management, RAG |
| LLM | OpenAI GPT-4o | via API | Best reasoning quality |
| STT | OpenAI Whisper | whisper-1 | Best accuracy |
| TTS | ElevenLabs | API v1 | Natural voice quality |
| Vector DB | ChromaDB | 0.5+ | Easy RAG implementation |
| Relational DB | PostgreSQL | 16 | Production-grade |
| ORM | SQLAlchemy | 2.x | Python standard |
| Code Sandbox | Docker | 24+ | Secure isolation |
| Auth | JWT + bcrypt | - | Secure authentication |
