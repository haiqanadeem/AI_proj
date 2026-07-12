# Postman Testing Guide - CodeSight AI Backend

This guide outlines the complete sequential testing flow to verify the CodeSight AI backend API before frontend integration.

## Pre-requisites & Environment Setup

1. **Start Services**: Ensure Docker Desktop is running.
   ```bash
   cd backend
   # Start postgres
   docker-compose up -d postgres
   
   # Start FastAPI server locally for development (or use docker-compose up backend)
   uvicorn app.main:app --reload
   ```

2. **Environment Variables**: Create a `backend/.env` file with at least:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   DATABASE_URL=postgresql://admin:password@localhost:5432/codesight
   JWT_SECRET=supersecretcodesightaijwtsecretkeysupersafe
   ```

3. **Postman Environment**: Create a Postman Environment with the following variables:
   - `base_url`: `http://localhost:8000`
   - `token`: *(leave blank, will be set after login)*
   - `lesson_id`: `1`

---

## 1. System Health Check

**Request**: `GET {{base_url}}/health`
- **Purpose**: Verify DB, ChromaDB, and Gemini API are connected.
- **Expected Response (200 OK)**:
  ```json
  {
    "status": "ok",
    "db": "ok",
    "chroma": "ok",
    "gemini": "ok"
  }
  ```
- **Assertions**:
  - `pm.response.to.have.status(200);`
  - `pm.expect(pm.response.json().db).to.eql("ok");`
  - `pm.expect(pm.response.json().gemini).to.eql("ok");`

---

## 2. Authentication Flow

### A. Register New User
**Request**: `POST {{base_url}}/auth/register`
- **Body** (JSON):
  ```json
  {
    "name": "Test Student",
    "email": "student@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Expected Response (201 Created)**: Returns user object.

### B. Login User
**Request**: `POST {{base_url}}/auth/login`
- **Body** (x-www-form-urlencoded):
  - `username`: `student@example.com`
  - `password`: `SecurePassword123!`
- **Expected Response (200 OK)**:
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user": { ... }
  }
  ```
- **Post-Request Script** (Add this in Postman `Tests` tab to auto-set token):
  ```javascript
  var jsonData = pm.response.json();
  pm.environment.set("token", jsonData.access_token);
  ```

---

> **IMPORTANT**: All subsequent requests must include the header:
> `Authorization: Bearer {{token}}`

---

## 3. Curriculum & Lessons

### A. Get All Lessons
**Request**: `GET {{base_url}}/lessons`
- **Purpose**: Verify that `seed.py` successfully populated the database.
- **Expected Response (200 OK)**: Array of 22 lesson objects.

### B. Get Specific Lesson
**Request**: `GET {{base_url}}/lessons/1`
- **Expected Response (200 OK)**: Returns the "Variables and Data Types" lesson.

---

## 4. Voice Intent & Tutor (AI Modules)

### A. Voice Intent Classification
**Request**: `POST {{base_url}}/ai/classify-intent`
- **Body** (JSON):
  ```json
  {
    "transcript": "what is a variable in python"
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "intent": "ASK_TUTOR",
    "params": {
      "question": "what is a variable in python"
    },
    "confidence": 0.9
  }
  ```

### B. Chat with AI Tutor (RAG)
**Request**: `POST {{base_url}}/tutor/chat`
- **Body** (JSON):
  ```json
  {
    "message": "what is a variable in python?",
    "lesson_id": 1,
    "topic_context": "Variables"
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "response": "A variable is like a labeled box where you store data...",
    "audio_url": null
  }
  ```
- **Assertions**: Verify the response is plain text without markdown (optimized for audio).

---

## 5. Code Execution & Analysis Sandbox

### A. Execute Safe Code
**Request**: `POST {{base_url}}/code/execute`
- **Body** (JSON):
  ```json
  {
    "code": "name = 'CodeSight'\nprint('Hello ' + name)",
    "language": "python",
    "lesson_id": 1
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "stdout": "Hello CodeSight\n",
    "stderr": "",
    "exit_code": 0,
    "execution_time_ms": 150
  }
  ```
- **Assertions**: `exit_code` must be 0, `stdout` must match.

### B. Execute Malicious Code (Security Test)
**Request**: `POST {{base_url}}/code/execute`
- **Body** (JSON):
  ```json
  {
    "code": "import os\nos.system('rm -rf /')",
    "language": "python"
  }
  ```
- **Expected Response**: Should fail harmlessly or return permission denied within the isolated docker container. The host OS must be untouched.

### C. Analyze Erroneous Code
**Request**: `POST {{base_url}}/code/analyze`
- **Body** (JSON):
  ```json
  {
    "code": "print('Hello world)",
    "execution_error": "SyntaxError: unterminated string literal",
    "lesson_id": 1
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "has_errors": true,
    "errors": [
      {
        "type": "SyntaxError",
        "description": "You forgot to close the quotation mark at the end of the string.",
        "line": 1,
        "fix": "print('Hello world')"
      }
    ],
    "positive_feedback": "You correctly used the print statement.",
    "spoken_summary": "There is a SyntaxError. You forgot to close the quotation mark. The correct code is print open parenthesis quote Hello world quote close parenthesis."
  }
  ```

---

## 6. Telemetry & Progress

### A. Create Voice Log
**Request**: `POST {{base_url}}/voice-logs`
- **Body** (JSON):
  ```json
  {
    "command": "run my code",
    "intent_detected": "SUBMIT_CODE",
    "confidence_score": 0.95,
    "execution_time_ms": 1200
  }
  ```
- **Expected Response (201 Created)**: Returns saved log.

### B. Get Progress Summary
**Request**: `GET {{base_url}}/progress`
- **Expected Response (200 OK)**:
  Returns calculated progress, knowledge profile, and a machine learning predicted completion rate via `progress_predictor.py`.

---

## ✅ Backend Ready for Frontend Checklist
- [x] Rate limiting is active (FastAPI slowapi).
- [x] All Gemini AI endpoints are active with strict JSON responses.
- [x] Code Sandbox strictly uses Docker isolation (no subprocess fallbacks).
- [x] Auth system issues JWT correctly.
- [x] Database is seeded with 22 lessons.
- [x] ChromaDB vector store is populated without mock embeddings.
