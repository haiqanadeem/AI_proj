# API Specification Document
## CodeSight AI — REST API Reference

**Version:** 1.0  
**Base URL:** `http://localhost:8000` (development)  
**Authentication:** Bearer JWT Token (except /auth endpoints)  
**Content-Type:** `application/json`

---

## Authentication

All protected endpoints require:
```
Authorization: Bearer <jwt_token>
```

---

## 1. Authentication Endpoints

### POST /auth/register
Register a new student account.

**Request:**
```json
{
  "name": "Ahmed Hassan",
  "email": "ahmed@example.com",
  "password": "SecurePass123"
}
```

**Response 201:**
```json
{
  "id": 1,
  "name": "Ahmed Hassan",
  "email": "ahmed@example.com",
  "level": "beginner",
  "created_at": "2025-06-01T10:00:00Z"
}
```

**Errors:**
- `400` — Email already registered
- `422` — Validation error (invalid email, weak password)

---

### POST /auth/login
Authenticate and receive JWT token.

**Request:**
```json
{
  "email": "ahmed@example.com",
  "password": "SecurePass123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Ahmed Hassan",
    "level": "beginner"
  }
}
```

**Errors:**
- `401` — Invalid credentials

---

### GET /auth/me
Get current authenticated user profile.

<truncated 6832 bytes>
: 
### GET /progress
Get current student's full progress.

**Response 200:**
```json
{
  "user_id": 1,
  "overall_completion": 33.3,
  "lessons_completed": 5,
  "lessons_total": 15,
  "knowledge_profile": {
    "Variables": 85.0,
    "Data Types": 72.0,
    "Loops": 45.0,
    "Functions": 0.0
  },
  "completion_prediction": 68.5,
  "at_risk": false,
  "spoken_summary": "You have completed 5 out of 15 lessons. Your strongest topic is Variables at 85 percent. Loops needs more practice at 45 percent. Keep going — you are doing great!"
}
```

---

### GET /progress/recommend
Get next recommended lesson.

**Response 200:**
```json
{
  "recommended_lesson": {
    "id": 4,
    "title": "Loops — Repeating Actions",
    "topic": "Loops",
    "difficulty": "beginner"
  },
  "reason": "Your mastery of Loops is 45% — below the 60% threshold. Reviewing this topic will strengthen your foundation.",
  "spoken_recommendation": "Based on your progress, I recommend reviewing Loops. You scored 45 percent mastery there. Say Open Loops Lesson to continue."
}
```

---

## Error Response Format

All errors follow this format:
```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2025-06-01T10:00:00Z"
}
```

## HTTP Status Codes Used

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request / validation error |
| 401 | Unauthorized (no or invalid JWT) |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Unprocessable entity |
| 429 | Rate limited (AI API) |
| 500 | Internal server error |
| 503 | AI service unavailable |
