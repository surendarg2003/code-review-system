# 🔍 AI-Powered Code Review Assistant

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F57C00?style=for-the-badge)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Deployed](https://img.shields.io/badge/Live-HF%20Spaces-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/novasurendar/code-review-assistant)

> A production-ready, streaming-capable AI code reviewer that instantly analyzes code for bugs, security vulnerabilities, style violations, and complexity issues. Returns structured JSON with actionable fixes and fully refactored code.

🔗 **Live Demo:** [https://huggingface.co/spaces/novasurendar/code-review-assistant](https://huggingface.co/spaces/novasurendar/code-review-assistant)

---

## ✨ Features

- 🌐 **Multi-Language Support**: Python, JavaScript, SQL, TypeScript, Java, Go, Rust, C#, C++
- 🛡️ **Security & Bug Detection**: Identifies injection flaws, unsafe practices, and logical errors
- 📐 **Style & Complexity Analysis**: Enforces PEP8/clean code standards, flags deep nesting & anti-patterns
- 📦 **Structured JSON Output**: Machine-readable `summary`, `issues[]`, and `refactored_code`
- ⚡ **Real-Time Streaming**: Token-by-token output via Server-Sent Events (SSE)
- 🐳 **Production-Ready**: Dockerized backend + frontend, CORS, health checks, robust fallback parsing
- ☁️ **One-Click Deploy**: Optimized for Hugging Face Spaces with environment secret management

---

## 🏗️ Architecture Pipeline

👤 User (Streamlit UI)
↓ [POST /api/review | JSON: {code, language}]
⚙️ Backend Gateway (FastAPI)
↓ [Validate → CORS → Pydantic Schema]
🤖 LLM Client (Groq SDK)
↓ [Prompt + JSON Schema Enforcement]
📦 Response Parser
↓ [json.loads() → Regex Fallback → Error Wrapping]
🔙 Structured JSON Response
🖥️ Frontend Renderer (Streamlit)
✅ Summary + Expandable Issues + Refactored Code


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Uvicorn, Pydantic, Groq Python SDK |
| **Frontend** | Streamlit, Requests, Native CSS/Markdown rendering |
| **Infrastructure** | Docker, Docker Compose, Hugging Face Spaces |
| **LLM** | Llama-3.3-70B-Instruct via Groq (configurable via `.env`) |
| **Deployment** | CPU-optimized container, HF Secrets for API keys |

---

## 🚀 Quick Start

### 📦 Prerequisites
- Python 3.9+
- `pip` & `virtualenv` (recommended)
- Docker & Docker Compose (optional)
- A [Groq API Key](https://console.groq.com/keys) (Free tier: ~500K tokens/day)

### 💻 Local Setup (Manual)
```bash
# 1. Clone & navigate
git clone <your-repo-url>
cd code-review-assistant

# 2. Create environment file
echo "GROQ_API_KEY=gsk_your-key-here" > backend/.env
echo "MODEL_NAME=llama-3.3-70b-versatile" >> backend/.env

# 3. Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && pip install -r requirements.txt

# 4. Run Backend (Terminal 1)
cd backend && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Run Frontend (Terminal 2)
cd frontend && BACKEND_URL=http://localhost:8000 python3 -m streamlit run app.py

🐳 Docker Setup

# Create .env in root with GROQ_API_KEY
docker compose up --build
# UI: http://localhost:8501 | API: http://localhost:8000/docs

☁️ Deploy to Hugging Face Spaces
Create a new Space on HF Spaces
Select Docker as the SDK
Upload all project files & push to the Space repo
Go to Settings → Repository secrets and add:
GROQ_API_KEY: gsk_...
The Space auto-builds via Dockerfile + start.sh. Access via your Space URL.

Request Schema:
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}

Response Schema:

{
  "summary": "Functional but lacks type hints and documentation.",
  "issues": [
    {
      "type": "style",
      "line": 1,
      "description": "Missing type annotations.",
      "severity": "low",
      "suggestion": "Add -> int and parameter types."
    }
  ],
  "refactored_code": "def add(a: int, b: int) -> int:\n    return a + b"
}

🧪 Why This Stands Out for Portfolios
✅ Real Engineering Pain Point: Automates a daily bottleneck every dev team faces
✅ Production-Grade Patterns: JSON schema enforcement, robust error fallbacks, CORS, health checks
✅ Interview-Ready Demo: Live streaming, structured output, multi-language support
✅ Clean Architecture: Decoupled backend/frontend, environment-driven configuration, Docker-ready

📄 License
This project is licensed under the MIT License.
🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Built by Surendar
