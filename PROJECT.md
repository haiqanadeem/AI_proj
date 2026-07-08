# Project: CodeSight AI

## Architecture
Three-tier architecture: Next.js 14 frontend → FastAPI backend → PostgreSQL + ChromaDB

### Tech Stack
- Frontend: Next.js 14, TypeScript, Tailwind CSS, ShadCN/UI
- Backend: FastAPI, Python 3.11+, SQLAlchemy 2.x
- Database: PostgreSQL 16 (Docker), ChromaDB (persistent, local)
- AI: Google Gemini (gemini-2.0-flash) primary, OpenAI Whisper fallback STT
- STT: Browser Web Speech API (primary), OpenAI Whisper (fallback)
- TTS: Browser Web Speech Synthesis API
- Code Sandbox: Docker python:3.11-slim
- Auth: JWT (python-jose) + bcrypt

### API Keys (via .env)
- GOOGLE_API_KEY=google_api_key
- OPENAI_API_KEY=openai_api_key

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Foundation & Infrastructure | Docker Compose, .env, project scaffolding, PostgreSQL setup, DB models, seed data | none | PLANNED |
| 2 | Backend Core | All FastAPI endpoints (auth, lessons, quiz, voice, code, tutor, progress), all 7 AI modules, Docker sandbox | M1 | PLANNED |
| 3 | Frontend Core | All Next.js pages, voice hooks, TTS/STT, contexts, UI components, API client | M1 | PLANNED |
| 4 | Integration & E2E Flow | Connect frontend to backend, full demo flow, fix integration bugs | M2, M3 | PLANNED |
| 5 | Accessibility & Polish | WCAG
<truncated 5082 bytes>
   │   ├── lessons/
│   │   │   ├── page.tsx
│   │   │   └── [lessonId]/page.tsx
│   │   ├── quiz/page.tsx
│   │   ├── code-lab/page.tsx
│   │   └── tutor/page.tsx
│   ├── components/
│   │   ├── voice/
│   │   │   ├── VoiceButton.tsx
│   │   │   ├── VoiceStatusBar.tsx
│   │   │   └── CommandDisplay.tsx
│   │   ├── tutor/
│   │   │   ├── ChatWindow.tsx
│   │   │   └── MessageBubble.tsx
│   │   ├── lessons/
│   │   │   ├── LessonCard.tsx
│   │   │   ├── LessonReader.tsx
│   │   │   └── ProgressBar.tsx
│   │   ├── quiz/
│   │   │   ├── QuizCard.tsx
│   │   │   └── AnswerOptions.tsx
│   │   ├── code/
│   │   │   ├── CodeEditor.tsx
│   │   │   └── OutputPanel.tsx
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── SkipToContent.tsx
│   │   │   └── KeyboardShortcuts.tsx
│   │   └── ui/                 # ShadCN components
│   ├── hooks/
│   │   ├── useVoiceRecognition.ts
│   │   ├── useTTS.ts
│   │   ├── useVoiceCommands.ts
│   │   └── useAuth.ts
│   ├── contexts/
│   │   ├── VoiceContext.tsx
│   │   ├── AuthContext.tsx
│   │   └── LessonContext.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── voice.ts
│   └── lib/
│       ├── intentParser.ts
│       └── accessibility.ts
└── files/                      # Spec docs (read-only reference)
```
