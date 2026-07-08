# Original User Request

## Initial Request — 2026-06-30T18:29:56+05:00

Build **CodeSight AI** — a production-ready, voice-first programming learning platform for visually impaired students. It's a full-stack web app with a Next.js 14 frontend, FastAPI Python backend, PostgreSQL database, and 7 distinct AI modules. The platform teaches Python programming entirely through voice interaction — no mouse or visual interaction required. This is a university AI course project that must demonstrate real AI depth (RAG, NLP, ML, code sandboxing) and be defensible in an academic viva.

Working directory: c:\Users\MuBeeN\Desktop\haiqa
Integrity mode: development

## Reference Documentation

Complete project specifications are in `c:\Users\MuBeeN\Desktop\haiqa\files\`:
- `01_PRD_Product_Requirements_Document.md` — Full product requirements
- `02_SRS_Software_Requirements_Specification.md` — Detailed system requirements (IEEE 830)
- `03_Architecture_Design_Document.md` — Three-tier architecture, directory structures, code samples
- `04_Database_Design_Document.md` — All PostgreSQL tables with CREATE TABLE statements, ChromaDB collections
- `05_AI_Design_Document.md` — All 7 AI modules with prompts, algorithms, and viva defense guide
- `06_10Day_Implementation_Plan.md` — Day-by-day build plan
- `07_API_Specification.md` — All REST endpoints with request/response JSON
- `08_Accessibility_and_Risk_Assessment.md` — WCAG 2.1 AA compliance spec, risk matrix

**READ ALL OF THESE FILES BEFORE STARTING.** They contain the complete architecture, database schemas, API contracts, AI prompts, and system design.

## API Keys (Environment Variables)

```
GOOGLE_API_KEY =your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Cost Strategy**: Use Google Gemini (`gemini-2.0-flash`) as the PRIMARY LLM for all AI modules (tutor, quiz gen, code analysis, intent classification) to minimize OpenAI costs. Use OpenAI ONLY for Whisper STT (if browser Web Speech API is insufficient) and as a fallback. Use free browser-native Web Speech API for STT and Web Speech Synthesis for TTS instead of paid ElevenLabs.

## Requirements

### R1. Full-Stack Application Foundation
Build a complete full-stack web application with:
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and ShadCN/UI components
- **Backend**: FastAPI (Python 3.11+) with SQLAlchemy ORM
- **Database**: PostgreSQL 16 (via Docker) with all tables from the Database Design Document (users, lessons, progress, quiz_attempts, chat_history, voice_logs, code_submissions, knowledge_profiles)
- **Authentication**: JWT-based auth with bcrypt password hashing, register/login endpoints
- All API endpoints from the API Specification document must be implemented and working

### R2. Voice-First Interface (Core Feature)
The entire platform must be operable through voice alone:
- **Speech-to-Text**: Use browser's Web Speech API (free) as primary, with OpenAI Whisper as fallback
- **Text-to-Speech**: Use browser's Web Speech Synthesis API (free) for all spoken feedback
- **Voice Intent Classification**: AI-powered NLP that classifies spoken commands into structured intents (NAVIGATE_HOME, OPEN_LESSON, START_QUIZ, ASK_TUTOR, etc.) using Google Gemini
- **Voice commands** must trigger navigation, lesson reading, quiz taking, code submission, and progress review
- Audio confirmation after every command

### R3. Seven AI Modules (Academic Showcase)
All 7 AI modules specified in the AI Design Document must be implemented and demonstrable:

1. **Conversational Tutor** — LLM-powered tutor with RAG context injection, using Google Gemini
2. **Adaptive Learning Engine** — Knowledge tracing with mastery score computation (formula: mastery = quiz_avg*0.6 + completion*0.3 + error_free*0.1), lesson recommendations based on weak topics
3. **Voice Intent Classifier** — Zero-shot NLP classification of voice commands into structured intent JSON using Gemini
4. **Code Analyzer** — Docker sandbox execution (python:3.11-slim, network disabled, 256MB, 10s timeout) + AI error explanation
5. **Quiz Generator** — Dynamic quiz generation via Gemini with constrained JSON output (3 MCQs, 1 code completion, 1 debug per quiz)
6. **Progress Predictor** — Logistic Regression ML model (sklearn) predicting student completion likelihood
7. **RAG Knowledge Base** — ChromaDB vector store with lesson content chunked and embedded, semantic search retrieval injected into tutor prompts

### R4. WCAG 2.1 Level AA Accessibility
- 100% keyboard navigable (Tab, Enter, Space, Arrow keys, Escape)
- All interactive elements have aria-labels, aria-live regions for dynamic content
- Skip-to-main-content links, visible focus rings (3px), semantic HTML5
- 4.5:1 contrast ratio minimum
- Compatible with NVDA/JAWS screen readers
- No time limits on user actions
- Full keyboard shortcut panel (Alt+V for voice, Alt+R for repeat, etc.)

### R5. Production Quality & Security
- All passwords hashed with bcrypt (never plain text)
- JWT tokens with proper expiration
- Docker code sandbox fully isolated (no network, readonly FS, resource limits)
- API keys in .env files, never committed to git
- CORS configured for frontend origin only
- Proper error handling with spoken error messages
- Loading states, form validation, and graceful degradation
- Professional, polished UI with high-contrast theme suitable for low-vision users

### R6. Lesson Content & Seeding
- Minimum 15 Python lessons across 3 difficulty tiers (Beginner: 6, Intermediate: 5, Advanced: 4)
- Each lesson has: title, concept explanation, code example, real-world analogy, common mistakes
- Lessons seeded into PostgreSQL on startup
- Lesson content chunked and embedded into ChromaDB for RAG retrieval
- Progress tracking per lesson per user

## Acceptance Criteria

### Application Runs Successfully
- [ ] `docker-compose up -d` starts PostgreSQL without errors
- [ ] `uvicorn app.main:app --reload` starts the FastAPI backend on port 8000
- [ ] `npm run dev` starts the Next.js frontend on port 3000
- [ ] Frontend loads at http://localhost:3000 without console errors

### Authentication Works
- [ ] POST /auth/register creates a new user and returns user JSON
- [ ] POST /auth/login returns a valid JWT token
- [ ] Protected endpoints reject requests without valid JWT
- [ ] Passwords are stored as bcrypt hashes (verify by checking DB)

### Voice System Works
- [ ] Clicking the microphone button activates speech recognition
- [ ] Spoken commands are transcribed to text (via Web Speech API)
- [ ] Transcribed text is classified into correct intents (test: "Open Python basics" → OPEN_LESSON)
- [ ] Intent execution navigates to correct page or triggers correct action
- [ ] TTS reads confirmation messages aloud after each command

### AI Modules Are Functional
- [ ] Tutor: Asking "What is a variable?" returns a RAG-grounded answer using lesson content
- [ ] Quiz: POST /quiz/generate returns 5 valid questions in correct JSON schema
- [ ] Code Analyzer: Submitting `for i in range(5)\n    print(i)` returns error explanation mentioning missing colon
- [ ] Adaptive: After quiz completion, the system recommends a next lesson based on mastery scores
- [ ] Progress Predictor: GET /progress returns completion_prediction score
- [ ] RAG: ChromaDB collection contains embedded lesson chunks (verify collection count > 0)
- [ ] Intent Classifier: 5 different voice commands all classify correctly

### Accessibility
- [ ] Every page has unique <title> tag
- [ ] Tab key navigates through all interactive elements in logical order
- [ ] All buttons and inputs have aria-labels
- [ ] Dynamic content updates announced via aria-live regions
- [ ] Skip-to-content link is first focusable element on every page
- [ ] Focus ring is visible on all focused elements

### Code Sandbox Security
- [ ] Docker container runs with network_disabled=True
- [ ] Docker container has read_only=True filesystem
- [ ] Container is removed after execution (remove=True)
- [ ] Execution times out after 10 seconds
- [ ] Memory limited to 256MB

### Database
- [ ] All 8 tables exist in PostgreSQL with correct schemas
- [ ] Foreign key constraints are in place
- [ ] Lesson seed data populates on startup (15+ lessons)
- [ ] ChromaDB collection has embedded lesson chunks

### End-to-End Demo Flow
- [ ] Complete demo flow works: Register → Login → Open Lesson → Ask Tutor → Take Quiz → Submit Code → View Progress → Get Recommendation
- [ ] Each step in the flow produces correct responses
- [ ] Voice works throughout the flow
