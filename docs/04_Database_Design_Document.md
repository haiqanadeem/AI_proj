# Database Design Document
## CodeSight AI

**Version:** 1.0  
**Date:** June 2025  
**Database:** PostgreSQL 16

---

## 1. Entity Relationship Overview

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────────┐
│    users    │──────<│     progress     │>──────│    lessons      │
└─────────────┘       └──────────────────┘       └─────────────────┘
       │                                                   │
       │              ┌──────────────────┐                 │
       └─────────────<│  chat_history    │                 │
       │              └──────────────────┘                 │
       │                                                   │
       │              ┌──────────────────┐                 │
       └─────────────<│  quiz_attempts   │>───────────────┘
       │              └──────────────────┘
       │
       │              ┌──────────────────┐
       └────────
<truncated 8284 bytes>
ent stored in ChromaDB:
{
    "id": "lesson_1_chunk_3",
    "document": "A variable in Python stores a value. Think of it like a labeled box...",
    "metadata": {
        "lesson_id": 1,
        "lesson_title": "Variables and Data Types",
        "topic": "Variables",
        "difficulty": "beginner",
        "chunk_index": 3
    },
    "embedding": [0.123, -0.456, ...]   # 1536-dim vector from text-embedding-3-small
}
```

### Retrieval Query

```python
results = collection.query(
    query_texts=["What is a variable in Python?"],
    n_results=3,
    where={"difficulty": "beginner"}   # Optional filter by student level
)
```

---

## 4. Database Seeding Strategy

At application startup, `seed.py` performs:
1. Insert all lesson records into PostgreSQL `lessons` table
2. Split each lesson into 300-token chunks
3. Generate embeddings for each chunk via OpenAI
4. Upsert all chunks into ChromaDB `lesson_chunks` collection

This ensures RAG is immediately functional without manual setup.

---

## 5. Data Retention Policy

| Table | Retention |
|---|---|
| users | Indefinite |
| lessons | Indefinite (content managed by admin) |
| progress | Indefinite |
| quiz_attempts | 12 months |
| chat_history | 6 months (then archive) |
| voice_logs | 30 days (debugging only) |
| code_submissions | 6 months |

---

## 6. Indexes Summary

All foreign key columns are indexed. Additional indexes:
- `users.email` — for fast login lookup
- `lessons.difficulty`, `lessons.topic` — for filtered queries
- `progress.user_id` — for dashboard queries
- `chat_history(user_id, session_id)` — for session retrieval
- `voice_logs.user_id` — for analytics
