# CodeSight AI — Project Context Window

**Version:** 1.0  
**Last Updated:** July 2026  
**Purpose:** Single source of truth for long Cursor/agent sessions. Read this file before any implementation work.

---

## Table of Contents

1. [Project Identity](#1-project-identity)
2. [Non-Negotiable Constraints](#2-non-negotiable-constraints)
3. [Architecture Summary](#3-architecture-summary)
4. [Voice Behavior Specification](#4-voice-behavior-specification)
5. [Intent Ontology](#5-intent-ontology)
6. [AI Module Specifications](#6-ai-module-specifications)
7. [Database Schema Reference](#7-database-schema-reference)
8. [API Contract Summary](#8-api-contract-summary)
9. [Accessibility Requirements](#9-accessibility-requirements)
10. [Lesson Content Plan](#10-lesson-content-plan)
11. [Environment Variables](#11-environment-variables)
12. [Demo Script (Viva Flow)](#12-demo-script-viva-flow)
13. [Risk Mitigations](#13-risk-mitigations)
14. [Folder Structure Reference](#14-folder-structure-reference)
15. [Implementation Rules for Agents](#15-implementation-rules-for-agents)

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Name** | CodeSight AI |
| **Tagline** | Voice-first programming learning platform for visually impaired and blind students |
| **Core Goal** | Production-quality, fully functional, highly interactive demo for university viva — must feel like a real intelligent companion, not a rigid voice menu |
| **Language (v1)** | Pytho
<truncated 31955 bytes>
box, voice_log
│       ├── database/              # connection, vector_store, seed/
│       └── utils/
├── frontend/
│   ├── app/                       # layout.tsx, page.tsx (SPA shell)
│   ├── components/                # layout, voice, auth, lessons, tutor, quiz, code, dashboard, ui
│   ├── contexts/                  # Voice, Auth, Lesson, App
│   ├── hooks/                     # speech, wake word, TTS, voice commands, dictation, keyboard
│   ├── lib/                       # intentRouter, voicePhrases, dictationMap, accessibility, api
│   └── types/
├── .gitignore
└── README.md
```

Full inventory of every function/component: see `docs/function_inventory.md`.  
Phased build order: see `docs/roadmap.md`.

---

## 15. Implementation Rules for Agents

1. **Read this file first** at the start of any long session.
2. **Follow the local stack** — never introduce OpenAI/ElevenLabs as required dependencies.
3. **Voice-first** — every feature must work via voice AND keyboard.
4. **SPA pattern** — use `AppContext.setView()`, not Next.js multi-page routes for main navigation.
5. **Match existing conventions** — read surrounding code before adding new files.
6. **Minimal scope** — only implement what the current roadmap phase requires.
7. **Accessibility non-negotiable** — aria-live, labels, focus management on every new component.
8. **Log AI actions** — voice intents to `voice_logs`; RAG chunks to `chat_history.retrieved_chunks`.
9. **No secrets in git** — use `.env.example` templates only.
10. **Do not commit** unless explicitly asked by the user.

---

*End of context window. For function-level build list see `function_inventory.md`. For phase order see `roadmap.md`.*
