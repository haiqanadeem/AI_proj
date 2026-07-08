# 10-Day Implementation Plan
## CodeSight AI — Sprint Plan for University Submission

**Approach:** AI-Assisted Development (Claude, Cursor, GitHub Copilot)  
**Timeline:** 10 Days  
**Goal:** Working demo with all 7 AI modules demonstrable in viva

---

## CRITICAL MINDSET

You have 10 days. This means:
- Do NOT build everything perfectly — build everything DEMONSTRABLY
- Every day ends with something you can run and show
- Use AI tools to write 80% of the code
- You write the glue, the config, and the thinking

---

## AI Tools You Will Use

| Tool | What You Use It For |
|---|---|
| **Claude (this conversation)** | Architecture, full component code, debugging, prompts |
| **Cursor IDE** | Write full files via AI autocomplete; use "Composer" for multi-file tasks |
| **GitHub Copilot** | Inline code completion as you type |
| **ChatGPT** | Alternative second opinion when Claude is unclear |
| **v0.dev** | Generate Next.js UI components from descriptions |

### How to Use Claude Effectively for This Project

Copy this pattern every time:

```
"I am building CodeSight AI. I need you to write the complete [component/file/module].

Context:
- Tech stack: Next.js 14 + TypeScript, FastAPI, PostgreSQL, OpenAI, ChromaDB
- Current file structure: [paste your file tree]
- This file's job: [one sentence]

Requirements:
- [list exactly what it must do]

Write the complete file. No placeholders. Productio
<truncated 13467 bytes>
h stack, installation steps, demo GIF placeholder, and how to run locally."*

**Final Commit:** `feat: v1.0 complete — all AI modules working, demo flow verified`

---

## GitHub Workflow

### Branch Strategy
```
main                    ← Production-ready, always working
develop                 ← Integration branch
  └─ feature/auth       ← Day 2
  └─ feature/voice      ← Day 3
  └─ feature/lessons    ← Day 4
  └─ feature/tutor      ← Day 5
  └─ feature/quiz       ← Day 6
  └─ feature/code-lab   ← Day 7
  └─ feature/adaptive   ← Day 8
  └─ feature/a11y       ← Day 9
```

### Daily Commit Pattern
```bash
git add .
git commit -m "feat: [what works today]"
git push origin feature/[current-feature]
# At end of feature: create PR → merge to develop
# At end of project: merge develop → main
```

---

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| OpenAI API rate limits | Cache common responses; use gpt-3.5-turbo for non-critical calls |
| Docker not available | Pre-test Docker Desktop on your machine on Day 1 |
| Voice recognition fails in demo room | Have keyboard fallback for all voice actions |
| ChromaDB slow to initialize | Pre-seed database the night before demo |
| Time runs out | Priority order: Voice ✓ → Tutor ✓ → Quiz ✓ → Code ✓ → Adaptive |

---

## Minimum Viable Demo (If Time Runs Short)

If you only have 5 days, build ONLY these in order:
1. Auth (Day 1-2)
2. Voice Navigation (Day 3) — most impressive
3. AI Tutor with RAG (Day 4-5) — proves real AI
4. Quiz Generator (Day 6) — proves AI content generation

These 4 features alone are enough to defend as a genuine AI project.
