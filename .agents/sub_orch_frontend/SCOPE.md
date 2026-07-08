# Scope: Frontend Core (Milestone 3)

## Architecture
- Next.js 14 with App Router, TypeScript, Tailwind CSS
- Voice-first design using browser Web Speech API
- All API calls to FastAPI backend at http://localhost:8000
- WCAG 2.1 AA accessibility throughout

## Sub-Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| SM-1 | Project Setup & Foundation | Next.js init, config, services, lib, hooks, contexts | none | PLANNED |
| SM-2 | Layout & Core Components | Navbar, SkipToContent, KeyboardShortcuts, voice components, root layout | SM-1 | PLANNED |
| SM-3 | All Pages | All 10 pages (home, auth, dashboard, lessons, quiz, code-lab, tutor) | SM-1, SM-2 | PLANNED |
| SM-4 | Feature Components | tutor, lessons, quiz, code components | SM-1 | PLANNED |

## SM-1: Project Setup & Foundation
Files to create:
- `frontend/package.json` — Next.js 14 with all deps
- `frontend/tsconfig.json`
- `frontend/tailwind.config.ts` — high-contrast accessible theme
- `frontend/next.config.js`
- `frontend/postcss.config.js`
- `frontend/.env.local`
- `frontend/app/globals.css` — Tailwind imports + accessibility styles
- `frontend/services/api.ts` — Axios client with JWT interceptor
- `frontend/services/voice.ts` — Voice service abstraction
- `frontend/lib/intentParser.ts` — Intent routing
- `frontend/lib/accessibility.ts` — ARIA utilities
- `frontend/lib/utils.ts` — cn() utility for Tailwind
- `frontend/hooks/useVoiceRecognition.ts` — Web Speech API STT
- `frontend/hooks/useTTS.ts` — Web Speech Synthesis TTS
- `frontend/hooks/useVoiceCommands.ts` — STT + intent classification
- `frontend/hooks/useAuth.ts` — JWT token management
- `frontend/contexts/VoiceContext.tsx` — Global voice state
- `frontend/contexts/AuthContext.tsx` — Auth state
- `frontend/contexts/LessonContext.tsx` — Lesson state

## SM-2: Layout & Core Components
Files to create:
- `frontend/app/layout.tsx` — Root layout with providers, skip-to-content
- `frontend/components/layout/Navbar.tsx` — Accessible nav
- `frontend/components/layout/SkipToContent.tsx` — Skip link
- `frontend/components/layout/KeyboardShortcuts.tsx` — Shortcut panel
- `frontend/components/voice/VoiceButton.tsx` — Mic button + animation
- `frontend/components/voice/VoiceStatusBar.tsx` — Listening status
- `frontend/components/voice/CommandDisplay.tsx` — Command display

## SM-3: All Pages
Files to create:
- `frontend/app/page.tsx` — Home/landing
- `frontend/app/(auth)/login/page.tsx` — Login
- `frontend/app/(auth)/register/page.tsx` — Register
- `frontend/app/dashboard/page.tsx` — Dashboard
- `frontend/app/lessons/page.tsx` — Lesson library
- `frontend/app/lessons/[lessonId]/page.tsx` — Single lesson
- `frontend/app/quiz/page.tsx` — Quiz interface
- `frontend/app/code-lab/page.tsx` — Code editor
- `frontend/app/tutor/page.tsx` — Chat interface

## SM-4: Feature Components
Files to create:
- `frontend/components/tutor/ChatWindow.tsx`
- `frontend/components/tutor/MessageBubble.tsx`
- `frontend/components/lessons/LessonCard.tsx`
- `frontend/components/lessons/LessonReader.tsx`
- `frontend/components/lessons/ProgressBar.tsx`
- `frontend/components/quiz/QuizCard.tsx`
- `frontend/components/quiz/AnswerOptions.tsx`
- `frontend/components/code/CodeEditor.tsx`
- `frontend/components/code/OutputPanel.tsx`

## Interface Contracts

### API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

### Auth Endpoints
- POST /auth/register → {name, email, password} → {id, name, email, level, created_at}
- POST /auth/login → {email, password} → {access_token, token_type, user}
- GET /auth/me → Auth header → {id, name, email, level, last_login}

### Lesson Endpoints
- GET /lessons?difficulty=&topic= → {lessons: [...], total}
- GET /lessons/{lesson_id} → full lesson object

### Voice Endpoints
- POST /voice/transcribe → multipart audio → {transcript, confidence, duration_sec}
- POST /ai/classify-intent → {transcript} → {intent, params, confidence, raw_command}

### Tutor Endpoints
- POST /tutor/chat → {message, session_id, lesson_context} → {response, session_id, tokens_used, rag_sources}

### Quiz Endpoints
- POST /quiz/generate → {topic, difficulty, lesson_id} → quiz object
- POST /quiz/submit → {lesson_id, quiz_json, answers, time_taken_sec} → scored result

### Code Endpoints
- POST /code/execute → {code, language} → {stdout, stderr, exit_code, execution_time_ms}
- POST /code/analyze → {code, execution_error} → {has_errors, errors, positive_feedback, spoken_summary}

### Progress Endpoints
- GET /progress → full progress object
- GET /progress/recommend → recommendation object
