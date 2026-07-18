# CodeSight AI 🚀

CodeSight AI is a premium, interactive AI-powered learning tutor built with a Next.js frontend, a FastAPI backend, a PostgreSQL database, and a local ChromaDB vector database. It includes a voice command interface (STT/TTS), dynamic quizzes, and a secure Docker-based Python code sandbox for interactive learning.

---

## 🏗️ Project Architecture

*   **Frontend**: Next.js 14, TypeScript, Tailwind CSS, ShadCN/UI
*   **Backend**: FastAPI, SQLAlchemy (PostgreSQL 16)
*   **Vector DB (RAG)**: ChromaDB (stored locally under `backend/chroma_db`)
*   **AI Models**:
    *   **Primary LLM**: Google Gemini (`gemini-2.0-flash`) via `google-generativeai`
    *   **Fallback LLM**: OpenRouter (Qwen-2.5-72b-instruct)
    *   **STT**: Browser Web Speech API with OpenAI Whisper fallback
    *   **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)
*   **Sandbox**: Dockerized secure `python:3.11-slim` container for client code execution

---

## 📋 Prerequisites

Ensure you have the following installed on your machine:
*   [Node.js](https://nodejs.org/) (v18.x or later)
*   [Python](https://www.python.org/) (v3.11 or later)
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (required for code sandbox and PostgreSQL container)

---

## ⚙️ Environment Configuration

You must set up environment files for both the **Backend** and **Frontend** before running the application.

### 1. Backend Config
Create a `.env` file inside the `backend` folder:
```bash
cp backend/.env.example backend/.env
```
Open [backend/.env](file:///c:/Users/MuBeeN/Desktop/haiqa/backend/.env) and update the configuration:
```env
# Database (PostgreSQL 16)
DATABASE_URL=postgresql://admin:password@localhost:5432/codesight

# JWT Authentication
SECRET_KEY=generate_a_long_secure_random_string_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI Keys
GOOGLE_API_KEY=your_google_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional (Fallback STT)
OPENAI_API_KEY=your_openai_api_key

# CORS
CORS_ORIGINS=http://localhost:3000
ENV=development
```

### 2. Frontend Config
Create a `.env.local` file inside the `frontend` folder:
```bash
# Inside frontend directory
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 How to Run the Application

You can spin up the application in two ways: using **Docker Compose** (simplest) or running the services **Locally** (native).

### Option A: Run via Docker Compose (Recommended)
This launches all required services, including the PostgreSQL database, and backend container:

1. Make sure Docker Desktop is running.
2. From the project root, run:
   ```bash
   docker compose up --build
   ```
3. The services will be accessible at:
   *   **Frontend**: `http://localhost:3000`
   *   **Backend API & Docs**: `http://localhost:8000/docs`

---

### Option B: Run Locally (Native)

#### Step 1: Start PostgreSQL DB
If not running the whole stack in Docker, you should still spin up the Postgres database container:
```bash
docker compose up postgres -d
```
*(Or use a locally installed PostgreSQL database running on port 5432).*

#### Step 2: Configure & Start Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The backend will start, seed database tables, populate lesson metadata, and initialize the ChromaDB vector database.

#### Step 3: Configure & Start Frontend
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node modules:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:3000` in your web browser.

---

## 🧪 Verification & Testing

Verify that your local backend installation is working correctly by running the integration tests.

With the virtual environment active, run from the `backend` directory:
```bash
python test_backend.py
```
This runs four verification tests:
1. **DB Test**: Verifies connection and ensures seed data has been correctly inserted.
2. **Voice Intent Test**: Validates the NLP parser for voice commands.
3. **RAG Test**: Queries the ChromaDB vector store for content retrieval.
4. **Quiz Gen Test**: Generates a test quiz using the active LLM provider.

---

## 🛠️ Troubleshooting

### Hugging Face DNS Connection Failures (`[Errno 11001] getaddrinfo failed`)
If the server crashes during startup with the following error:
```text
'[Errno 11001] getaddrinfo failed' thrown while requesting HEAD https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/...
❌ Failed to initialize ChromaDB: Cannot send a request, as the client has been closed.
```
This happens if your network or ISP blocks `huggingface.co` or has temporary DNS resolution issues.

**Solution (Run Offline):**
If you have successfully run the project before, the model is already cached on your machine and you don't need to re-download anything. Update your backend `.env` file to enable offline mode:
```env
HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
```
This forces the application to load the model from your local cache directory (`~/.cache/huggingface`) without attempting any network connection.

### Code Sandbox Docker Requirements
The Python Code Lab executing user code uses a containerized sandbox. 
*   Ensure **Docker Desktop** is open and running on your system before typing code in the frontend lab.
*   If running backend locally, ensure your user has permissions to access the docker daemon (`docker ps` should work in your terminal).