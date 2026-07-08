# CodeSight AI
### Voice-First Programming Learning Platform for Visually Impaired Students

> An AI-powered educational platform that teaches programming from beginner to advanced level entirely through voice interaction — no mouse, no visual interface required.

---

## Project Documents (Read Before Coding)

| # | Document | Purpose |
|---|---|---|
| 01 | [PRD — Product Requirements](docs/01_PRD_Product_Requirements_Document.md) | What we are building and why |
| 02 | [SRS — Software Requirements](docs/02_SRS_Software_Requirements_Specification.md) | Every system requirement in detail |
| 03 | [Architecture Design](docs/03_Architecture_Design_Document.md) | System diagrams and tech decisions |
| 04 | [Database Design](docs/04_Database_Design_Document.md) | All tables, schemas, indexes |
| 05 | [AI Design Document](docs/05_AI_Design_Document.md) | All 7 AI modules with prompts and algorithms |
| 06 | [10-Day Implementation Plan](docs/06_10Day_Implementation_Plan.md) | Day-by-day build plan using AI tools |
| 07 | [API Specification](docs/07_API_Specification.md) | All REST endpoints with request/response |
| 08 | [Accessibility & Risk Assessment](docs/08_Accessibility_and_Risk_Assessment.md) | WCAG 2.1 + risk mitigation |

---

## The 7 AI Modules

| Module | AI Technique | Purpose |
|---|---|---|
| Conversational Tutor | LLM (GPT-4o) | Answers programming questions in beginner language |
| Adaptive Learning | Knowledge Tracing + Rule Engine | Personalizes difficulty and lesson 
<truncated 346 bytes>
ession ML | Predicts student completion likelihood |
| RAG Knowledge Base | Vector Embeddings + ChromaDB | Grounds tutor answers in course content |

---

## Tech Stack

**Frontend:** Next.js 14 · TypeScript · Tailwind CSS · ShadCN/UI  
**Backend:** FastAPI · Python 3.11 · SQLAlchemy  
**AI:** OpenAI GPT-4o · Whisper STT · LangChain · ChromaDB  
**Database:** PostgreSQL 16  
**Voice:** ElevenLabs TTS (Web Speech API fallback)  
**Sandbox:** Docker python:3.11-slim  

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yourusername/codesight-ai
cd codesight-ai

# 2. Start database
docker-compose up -d

# 3. Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
uvicorn app.main:app --reload

# 4. Frontend
cd ../frontend
npm install
cp .env.example .env.local  # Add API URL
npm run dev
```

Visit http://localhost:3000

---

## Demo Flow (University Viva)

```
1. Open website → say "Register" → voice registration
2. Say "Login" → authenticated
3. Say "Open Python Basics" → lesson opens and reads aloud
4. Say "What is a variable?" → AI tutor answers via RAG
5. Say "Start Quiz" → AI generates quiz → answer by voice
6. Type code with error → say "Submit Code" → Docker runs it → AI explains error
7. Say "My Progress" → adaptive engine summarizes and recommends next lesson
```

---

## Accessibility

- WCAG 2.1 Level AA compliant
- Compatible with NVDA, JAWS, VoiceOver
- 100% keyboard navigable
- Full voice control without any visual interaction required

---

*Built for university AI course project — demonstrating real AI system design*
