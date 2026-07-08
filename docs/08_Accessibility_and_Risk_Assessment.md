# Accessibility Compliance Document
## CodeSight AI — WCAG 2.1 Level AA Specification

**Version:** 1.0  
**Standard:** Web Content Accessibility Guidelines (WCAG) 2.1  
**Target Level:** AA  
**Screen Readers Tested:** NVDA, JAWS, VoiceOver

---

## 1. Why Accessibility Is Central — Not Optional

CodeSight AI's primary user is a blind student. This is not a standard "accessible design checkbox" — it is the core product requirement. If the platform is not fully accessible, the product fails entirely.

This document defines how every WCAG 2.1 principle maps to a specific implementation in CodeSight AI.

---

## 2. WCAG 2.1 Principle Implementation

### Principle 1: PERCEIVABLE
*Information must be presentable in ways all users can perceive.*

| Guideline | Implementation |
|---|---|
| 1.1 Text Alternatives | All images have `alt` text. Icons have `aria-label`. Decorative images use `alt=""`. |
| 1.2 Time-based Media | No video content in v1. Audio lessons have text transcripts. |
| 1.3 Adaptable | Semantic HTML5 (`<main>`, `<nav>`, `<article>`, `<section>`). Logical reading order without CSS. |
| 1.4.1 Use of Color | Error states use icon + text, never color alone. Progress uses percentage text, not just color bar. |
| 1.4.3 Contrast Minimum | All text meets 4.5:1 contrast ratio minimum. Large text meets 3:1. |
| 1.4.4 Resize Text | All text scalable to 200% without horizontal scroll or content loss. |
| 1.4.10 Reflow | Content reflows 
<truncated 6487 bytes>
dules; have fallback demo plan |
| R7 | Academic rejection — "no real AI" | Low | Critical | High | AI Design Document prepared; 7 modules; RAG + ML model provable |
| R8 | TTS voice sounds robotic / unclear | Medium | Low | Low | ElevenLabs provides high-quality voice; Web Speech API as backup |

---

## Critical Risk Details

### R4 — Docker Code Execution Security

**Why This Is Critical:** Allowing students to run arbitrary code on a server is inherently dangerous. A malicious student could run `os.system("rm -rf /")` or attempt network attacks.

**Mitigation Implementation:**
```python
container = client.containers.run(
    image="python:3.11-slim",
    command=f'timeout 10 python3 -c "{escaped_code}"',
    mem_limit="256m",          # Memory limit
    cpu_quota=50000,           # 50% of one CPU
    network_disabled=True,     # No network access
    read_only=True,            # Readonly filesystem
    tmpfs={"/tmp": "size=64m"},# Only /tmp is writable
    user="nobody",             # Non-root user
    remove=True,               # Container deleted after run
    detach=False
)
```

### R7 — Academic Defense Preparation

**If professor says "this is just ChatGPT wrapped":**

Present the AI Design Document and demonstrate:
1. RAG — Ask "What is a variable?" and show ChromaDB retrieved chunks in the response
2. NLP — Say "Open Python Basics" and show the intent JSON classification  
3. ML — Show the knowledge profile and mastery score computation with the formula
4. Code Sandbox — Submit code with an error and show Docker execution separate from AI
5. Adaptive — Show how the recommendation changes after failing a quiz

These are five provably distinct AI/ML techniques that cannot be replicated by calling ChatGPT once.
