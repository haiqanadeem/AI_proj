# CodeSight AI — Implementation Roadmap

**Version:** 1.0  
**Last Updated:** July 2026  
**Timeline:** 12 days (Phases 0–6)  
**Goal:** Viva-ready demo with all 7 AI modules, voice-first UX, and WCAG 2.1 AA compliance

---

## Overview

This roadmap adapts the original 10-day plan to incorporate:

- **100% local/free AI stack** (Ollama, ChromaDB, browser STT/TTS)
- **SPA architecture** with React Contexts (not multi-page routing)
- **Always-listening wake word** ("Hey CodeSight" / "CodeSight")
- **Voice authentication** and **voice code dictation**
- **22 structured lessons** (12 beginner + 10 intermediate)

Each phase ends with a **demonstrable milestone** — something you can run and show.

---

## Phase Summary

| Phase | Days | Focus | Milestone |
|---|---|---|---|
| 0 | 0–1 | Documentation & scaffold | Health check passes; docs approved |
| 1 | 2–3 | Auth + voice foundation | Wake word → command → navigate view |
| 2 | 4–5 | Lessons + RAG | RAG-grounded tutor answer with sources |
| 3 | 6–7 | Tutor + quiz | Full lesson → quiz → spoken score |
| 4 | 8–9 | Code lab + dictation | Voice-written code submitted & analyzed |
| 5 | 10 | Adaptive + dashboard | Recommendation changes after weak quiz |
| 6 | 11–12 | A11y hardening + demo prep | 10-minute viva flow runs 5× cleanly |

---

## Phase 0 — Documentation & Scaffold (Days 0–1)

### Goals

- Establish project repository and documentation
- Cop
<truncated 14827 bytes>
| SpeechRecognition supported |

### Startup Order (Every Dev Session)

```bash
# 1. Database
docker-compose -f docker/docker-compose.yml up -d

# 2. Ollama (if not as service)
ollama serve

# 3. Backend
cd backend && uvicorn app.main:app --reload

# 4. Frontend
cd frontend && npm run dev
```

---

## Risk Register (Roadmap-Specific)

| Risk | Phase | Mitigation |
|---|---|---|
| Ollama model too slow | 1+ | Use llama3.1:8b not 70b; limit response tokens |
| Browser STT inaccurate | 1 | Push-to-talk; Whisper fallback in Phase 6 |
| Lesson content takes too long | 2 | AI-generate drafts; minimum 10 lessons for demo |
| Docker sandbox fails on Windows | 4 | Test Day 1; WSL2 backend for Docker |
| ChromaDB embed slow at seed | 2 | Run seed once; persist `./chroma_db` |
| Demo room noise | 6 | Push-to-talk toggle; keyboard cheat sheet |

---

## Definition of Done (Whole Project)

- [ ] All 198 function inventory items implemented or explicitly deferred
- [ ] All 7 AI modules demonstrable live
- [ ] 22 lessons seeded and RAG-indexed
- [ ] Voice-only demo flow completable without mouse
- [ ] WCAG 2.1 AA checklist passed
- [ ] README with setup instructions complete
- [ ] 10-minute viva script runs 5× without failure

---

## Next Step

**Await user approval of:**
1. `docs/context_window.md`
2. `docs/function_inventory.md`
3. `docs/roadmap.md`

After approval → begin **Phase 0 Day 1** scaffold tasks (backend + frontend shells).

**Do not generate application code until explicit approval is given.**

---

*Cross-references: `context_window.md` for specs; `function_inventory.md` for build checklist; source docs 01–08 for detailed requirements.*
