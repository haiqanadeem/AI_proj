# AI Design Document
## CodeSight AI — AI Systems Specification

**Version:** 1.0  
**Date:** June 2025  
**Purpose:** Full specification of all AI modules, models, prompts, and algorithms

---

## 1. AI Systems Overview

CodeSight AI implements **seven distinct AI modules**, each solving a different problem in the learning pipeline. This document is intentionally written to be presented in academic viva to demonstrate real AI depth.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CODESIGHT AI SYSTEMS MAP                     │
│                                                                 │
│  [Voice Input]                                                  │
│       │                                                         │
│       ▼                                                         │
│  MODULE 3: Voice Intent Classifier (NLP)                        │
│       │                                                         │
│       ├──► "Open Lesson" ──► Direct navigation                  │
│       │                                                         │
│       └──► "What is X?" ──► MODULE 1: Conversational Tutor      │
│                                    │                            │
│                   
<truncated 17608 bytes>
4. **It requires vector databases** — ChromaDB, FAISS, Pinecone
5. **It's domain-specific** — our RAG only knows our curriculum, not random internet content

---

## 9. Prompt Engineering Principles

All prompts in CodeSight AI follow these principles:

| Principle | Implementation |
|---|---|
| Clear role definition | Every prompt starts with "You are..." |
| Output format specification | All prompts requiring structured data specify exact JSON schema |
| Constraint enumeration | Rules listed explicitly, not implied |
| Audio optimization | All prompts remind model to generate audio-friendly text |
| Accessibility awareness | Prompts specify the student is visually impaired |
| Hallucination prevention | RAG context injected before question |
| Length control | Max token counts specified for audio delivery |

---

## 10. AI Defense Guide (Viva Preparation)

| Question | Answer Summary |
|---|---|
| "Where is the AI?" | 7 distinct AI modules: LLM tutor, RAG, NLP classifier, code analyzer, quiz generator, adaptive engine, ML predictor |
| "Is this just ChatGPT?" | No. RAG retrieves course-specific content. NLP classifies intents. ML predicts completion. Docker sandbox executes code. |
| "What is RAG?" | Retrieval Augmented Generation: retrieve relevant lesson chunks from vector DB, inject as LLM context, generate grounded answers |
| "What ML algorithms?" | Knowledge Tracing (mastery score), Logistic Regression (completion prediction), Collaborative Filtering (recommendations) |
| "How is this different from YouTube?" | Responds to questions, evaluates code, adapts difficulty, tracks progress, operates entirely through voice |
| "What if AI gives wrong answers?" | RAG grounds answers in lesson content. Code analyzer validates via actual execution, not just LLM guessing. |
