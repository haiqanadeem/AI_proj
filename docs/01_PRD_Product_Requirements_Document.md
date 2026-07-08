# Product Requirements Document (PRD)

## CodeSight AI — Voice-First Programming Learning Platform for Visually Impaired Students

**Document Version:** 1.0  
**Date:** June 2025  
**Status:** Approved for Development  
**Owner:** Project Team  
**Classification:** Internal

\---

## Table of Contents

1. Executive Summary
2. Problem Statement
3. Product Vision \& Goals
4. Target Users \& Personas
5. Functional Requirements
6. Non-Functional Requirements
7. AI System Requirements
8. Accessibility Requirements
9. Feature Prioritization (MoSCoW)
10. Success Metrics
11. Out of Scope
12. Assumptions \& Constraints
13. Dependencies

\---

## 1\. Executive Summary

CodeSight AI is a web-based, voice-first programming education platform purpose-built for visually impaired and blind students. The platform leverages multiple AI systems — including a conversational LLM tutor, adaptive learning engine, voice NLP command interpreter, AI code analyzer, and RAG-based knowledge retrieval — to deliver a fully accessible, personalized programming education experience from absolute beginner to advanced level.

Unlike generic ChatGPT wrapper applications, CodeSight AI integrates seven distinct AI modules in a cohesive learning pipeline that personalizes curriculum, evaluates student code, and navigates the entire interface through voice — requiring zero visual interaction.

\---

## 2\. Problem Statement

### 2.1 Th
<truncated 11538 bytes>
 Export progress as PDF

### Won't Have (Out of Scope for v1)

* Mobile native app
* Real-time collaboration
* Video content
* Payment/subscription system

\---

## 10\. Success Metrics

|Metric|Target|
|-|-|
|Voice command recognition accuracy|> 90%|
|AI tutor response relevance (manual eval)|> 85%|
|WCAG 2.1 AA audit pass rate|100%|
|Lesson completion via voice only|Fully achievable without mouse|
|AI modules demonstrable in viva|All 7 modules live and working|
|End-to-end demo flow completion|Under 10 minutes|

\---

## 11\. Out of Scope

* Native iOS / Android applications
* Support for languages other than Python (v1)
* Video-based lesson content
* Real-time multi-user features
* Teacher administrative portal (v1)
* Monetization or subscription billing

\---

## 12\. Assumptions \& Constraints

**Assumptions:**

* Students have access to a microphone-enabled device and modern browser
* OpenAI API access is available for the development and demo period
* Docker is available on the backend server for sandbox execution

**Constraints:**

* Development timeline: 10 days
* Team size: 1–2 developers
* Budget: Minimal (OpenAI API/GEMENI API free; free-tier hosting acceptable for demo)
* Must be demonstrable live in university viva setting

\---

## 13\. Dependencies

|Dependency|Type|Risk|
|-|-|-|
|OpenAI API availability|External|Medium — have fallback (local Ollama)|
|Whisper API accuracy|External|Low — well-tested|
|Docker sandbox security|Infrastructure|Medium — use pre-built sandbox image|
|ChromaDB vector store|Library|Low — well-documented|
|ElevenLabs TTS API|External|Low — Azure TTS as fallback|



