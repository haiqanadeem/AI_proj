# Software Requirements Specification (SRS)
## CodeSight AI — Voice-First Programming Learning Platform

**Document Version:** 1.0  
**Date:** June 2025  
**Standard:** IEEE 830 (adapted)

---

## 1. Introduction

### 1.1 Purpose
This SRS defines the complete functional and non-functional requirements for CodeSight AI. It serves as the contract between the design team and the development team, ensuring every implemented feature matches the documented intent.

### 1.2 Scope
CodeSight AI is a full-stack web application with:
- A Next.js frontend with voice-first accessibility
- A FastAPI Python backend
- An AI layer integrating OpenAI LLMs, Whisper STT, ChromaDB, and Docker code execution
- A PostgreSQL relational database

### 1.3 Definitions

| Term | Definition |
|---|---|
| STT | Speech-to-Text — converting spoken audio to transcribed text |
| TTS | Text-to-Speech — converting text output to spoken audio |
| RAG | Retrieval Augmented Generation — LLM answer generation grounded in retrieved documents |
| Intent | The classified purpose behind a voice command (e.g., OPEN_LESSON) |
| Knowledge Tracing | Tracking what concepts a student has learned and how well |
| Sandbox | An isolated execution environment for running untrusted student code |
| Vector DB | A database that stores text as numerical embeddings for semantic search |

---

## 2. System Overview

```
┌───────────
<truncated 10817 bytes>
anation SHALL be read aloud via TTS.

---

### 3.7 Adaptive Learning Engine Module

**REQ-AL-001:** The system SHALL maintain a knowledge profile for each student containing:
- Per-topic quiz scores (running average)
- Per-topic error counts from code analyzer
- Time spent per lesson
- Current recommended difficulty

**REQ-AL-002:** The system SHALL compute a mastery score (0–100) per topic based on the formula:

```
mastery = (quiz_avg * 0.6) + (completion_rate * 0.3) + (error_free_rate * 0.1)
```

**REQ-AL-003:** The system SHALL flag topics with mastery below 60% as "needs review."

**REQ-AL-004:** After every quiz or lesson completion, the system SHALL call the recommendation engine which returns the next recommended lesson.

**REQ-AL-005:** The recommendation SHALL be announced via voice: "Great work! Based on your progress, I recommend studying Functions next."

---

## 4. External Interface Requirements

### 4.1 OpenAI API
- Endpoint: `https://api.openai.com/v1`
- Models: `gpt-4o` (tutor, code analyzer, quiz), `whisper-1` (STT), `text-embedding-3-small` (RAG)

### 4.2 ElevenLabs TTS API
- Endpoint: `https://api.elevenlabs.io/v1/text-to-speech`
- Fallback: Web Speech API (browser-native, no API key required)

### 4.3 Docker Code Sandbox
- Image: `python:3.11-slim`
- Network: Disabled inside container
- Filesystem: Read-only with /tmp write access only

---

## 5. Constraints

- Backend must be Python (FastAPI) for AI library compatibility
- Frontend must be Next.js with TypeScript
- All AI API keys must be stored in environment variables; never committed to git
- Code execution sandbox must be isolated from host
- All external API calls must have timeout limits (max 30 seconds)
