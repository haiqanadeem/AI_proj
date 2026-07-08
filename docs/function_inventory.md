# CodeSight AI — Function Inventory

**Version:** 1.0  
**Last Updated:** July 2026  
**Purpose:** Numbered, hierarchical list of every function, component, hook, service, and API handler to be built. Use as a build checklist during implementation.

**Total items:** 198

---

## 1. Frontend — Voice Engine

### 1.1 Hooks — Speech Recognition

| ID | Function / Export | File | Description |
|---|---|---|---|
| 1.1.1 | `useSpeechRecognition()` | `hooks/useSpeechRecognition.ts` | Hook factory; returns recognition instance and state |
| 1.1.2 | `startContinuous()` | `hooks/useSpeechRecognition.ts` | Start listening with continuous=true, interimResults=true |
| 1.1.3 | `startSingleUtterance()` | `hooks/useSpeechRecognition.ts` | One-shot listen for command after wake word |
| 1.1.4 | `stopListening()` | `hooks/useSpeechRecognition.ts` | Abort recognition session cleanly |
| 1.1.5 | `onResult(callback)` | `hooks/useSpeechRecognition.ts` | Register handler for final + interim transcripts |
| 1.1.6 | `onError(callback)` | `hooks/useSpeechRecognition.ts` | Handle no-speech, not-allowed, network errors |
| 1.1.7 | `isSupported()` | `hooks/useSpeechRecognition.ts` | Check browser SpeechRecognition availability |
| 1.1.8 | `requestMicPermission()` | `hooks/useSpeechRecognition.ts` | getUserMedia wrapper with error messages |

### 1.2 Hooks — Wake Word

| ID | Function / Export | File | Description |
|---|---|---|---|
| 1.2.1 | `useWakeWord()` | `hooks/useWakeWord.ts` | H
<truncated 27724 bytes>
onse` | `schemas/progress.py` | Full progress API response |
| 8.1.11 | `RecommendResponse` | `schemas/progress.py` | recommended_lesson, spoken_recommendation |
| 8.1.12 | `HealthResponse` | `schemas/health.py` | status, db, ollama, chroma checks |

---

## 9. Frontend — Root App Files

| ID | Function / Export | File | Description |
|---|---|---|---|
| 9.1.1 | `RootLayout` | `app/layout.tsx` | HTML shell, providers, skip link, announcer |
| 9.1.2 | `HomePage` (SPA shell) | `app/page.tsx` | AppShell + ViewRouter entry point |
| 9.1.3 | `globals.css` | `app/globals.css` | Tailwind, focus rings, high-contrast vars |

---

## 10. DevOps & Config Files

| ID | File | Description |
|---|---|---|
| 10.1.1 | `docker/docker-compose.yml` | PostgreSQL 16 service |
| 10.1.2 | `backend/requirements.txt` | Python dependencies |
| 10.1.3 | `backend/.env.example` | Backend env template |
| 10.1.4 | `backend/Dockerfile` | Backend container build |
| 10.1.5 | `frontend/.env.example` | Frontend env template |
| 10.1.6 | `.gitignore` | Node, Python, .env, chroma_db exclusions |
| 10.1.7 | `README.md` | Project overview, setup, demo flow |

---

## Cross-Reference Index

| Source Document | Inventory Sections |
|---|---|
| PRD (01) | All sections — functional requirements mapped |
| SRS (02) | 1.x Voice, 2.x Views, 5.x AI modules |
| Architecture (03) | 2.x Views, 6.x Infrastructure, 9.x App files |
| Database (04) | 7.x Models, 6.2.x Vector store |
| AI Design (05) | 5.x AI Modules (all 7 modules) |
| API Spec (07) | 4.3.x, 5.x API routes, 8.x Schemas |
| Accessibility (08) | 3.x Accessibility, 1.8.x ARIA components |

---

*Total: 198 numbered items. Mark each complete during implementation phases defined in `roadmap.md`.*
