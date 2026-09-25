<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18%2B-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Vite-Frontend-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL 16">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/LangGraph-Agent%20Workflow-1C3C3C?style=for-the-badge" alt="LangGraph">
  <img src="https://img.shields.io/badge/LangChain-AI%20Integration-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/FastMCP-MCP%20Server-6C47FF?style=for-the-badge" alt="FastMCP">
</p>

<h1 align="center">Agent Evaluation System</h1>

<p align="center">
  A production-ready, full-stack AI Agent Management and Evaluation Platform engineered to configure, version, benchmark, and evaluate Large Language Model (LLM) agents against customizable qualitative and quantitative criteria.
</p>

---

## 📌 Project Overview

The **Agent Evaluation System** delivers a unified workspace bridging agent orchestration and rigorous evaluation:

- **Interactive React Dashboard**: Fast, modern frontend built with Vite and React for seamless workspace navigation, prompt versioning, criteria management, and live test evaluation runs.
- **High-Performance FastAPI Backend**: Robust REST API backed by LangChain, LangGraph, and Google Gemini LLMs to execute evaluation workflows against multi-dimensional quality rubrics.
- **Relational Persistence**: PostgreSQL stores projects, agent metadata, versioned system prompts, custom dimensions, and historical evaluation logs.

---

## ✨ Key Features

- 📁 **Project & Workspace Isolation**: Group related AI agents, prompt iterations, and evaluation criteria into distinct projects.
- 🤖 **Agent Management**: Create, update, and manage multiple specialized AI agents per workspace.
- 📝 **Prompt Version Control**: Iterate on system instructions with automated prompt versioning (`v1`, `v2`, etc.).
- 📐 **Custom Evaluation Dimensions**: Define tailored quality standards (e.g., *Accuracy*, *Tone*, *Safety*, *Completeness*) with custom descriptions.
- ⚡ **Live Agent Evaluation Pipeline**: Trigger real-time evaluation runs using Google Gemini LLM to obtain score breakdowns, qualitative reasoning, and overall ratings.
- 📊 **Evaluation History & Audit Logs**: Retain and review past evaluation runs with timestamps, test chats, and detailed assessment outputs.

---

## 🔄 Workflow Architecture

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Create Project  │ ───►  │ Add AI Agent    │ ───►  │ Define Prompt   │
└─────────────────┘       └─────────────────┘       └────────┬────────┘
                                                             │
┌─────────────────┐       ┌─────────────────┐                │
│ Track History   │ ◄───  │ Run Evaluation  │ ◄──────────────┘
│ & View Reports  │       │ (Gemini Engine) │   Setup Quality Criteria
└─────────────────┘       └─────────────────┘   (Custom Dimensions)
```

---

## 🛠️ Tech Stack

| Layer | Technologies | Description |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, Lucide React, CSS3 | Single-page application with responsive design and instant HMR |
| **Backend** | FastAPI, Uvicorn, Pydantic | Asynchronous Python REST API framework |
| **AI Orchestration** | LangChain, LangGraph, FastMCP | Agent execution and evaluation workflow pipelines |
| **LLM Engine** | Google Gemini (`gemini-2.5-flash` / `gemini-3.1-flash-lite`) | Generative evaluation and scoring model |
| **Database** | PostgreSQL 16 | Relational store for workspaces, agents, prompts, and logs |
| **Infrastructure** | Docker, Docker Compose | Containerized database and service deployment |

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: `3.10` or higher
- **Node.js**: `v18+` & **npm**: `v9+`
- **Docker Desktop** or **Docker Engine**
- **Google Gemini API Key**

---

### Step 1: Clone & Configure Environment

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Mit-007/Agent-Evaluation-System-.git
   cd Agent-Evaluation-System-
   ```

2. Create a root `.env` file for the backend:
   ```env
   # =====================
   # Database Setup
   # =====================
   HOST="localhost"
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="your_postgres_password"
   POSTGRES_DB="agent_evaluation"
   PORT=5432

   # =====================
   # LLM & AI Configuration
   # =====================
   GOOGLE_API_KEY="your_google_gemini_api_key"
   LLM_MODEL_NAME="gemini-2.5-flash"
   TEMPERATURE=0
   ```

3. Create the frontend environment file inside `frontend/.env`:
   ```env
   VITE_API_BASE_URL=/api
   ```

---

### Step 2: Start PostgreSQL (Docker Compose)

Start the PostgreSQL 16 database container:
```bash
docker compose up -d
```

Verify the container status:
```bash
docker compose ps
```

---

### Step 3: Setup & Run FastAPI Backend

1. Create and activate a Python virtual environment:
   ```powershell
   # Windows PowerShell
   python -m venv myvenv
   .\myvenv\Scripts\Activate.ps1
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

- **Backend API**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

### Step 4: Setup & Run React Frontend

In a separate terminal window:

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit:
   ```text
   http://localhost:5173
   ```

---

## 📡 API Endpoints Reference

### 📁 Projects (`/projects`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/projects` | Retrieve all projects |
| `POST` | `/projects` | Create a new project |
| `GET` | `/projects/{project_id}` | Retrieve single project details |
| `PUT` | `/projects/{project_id}` | Update project name |
| `DELETE` | `/projects/{project_id}` | Delete project and cascade items |

### 🤖 Agents (`/agents`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/projects/{project_id}/agents` | Create an agent under a project |
| `GET` | `/projects/{project_id}/agents` | List all agents for a project |
| `GET` | `/agents/{agent_id}` | Get agent details |
| `PUT` | `/agents/{agent_id}` | Update agent name |
| `DELETE` | `/agents/{agent_id}` | Delete an agent |

### 📝 Prompts (`/prompts`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/agents/{agent_id}/prompts` | Create new prompt version for agent |
| `GET` | `/agents/{agent_id}/prompts` | List all prompt versions for an agent |
| `GET` | `/agents/{agent_id}/prompts/latest` | Get the latest active prompt |
| `GET` | `/prompts/{prompt_id}` | Get specific prompt by ID |
| `PUT` | `/prompts/{prompt_id}` | Update prompt content |
| `DELETE` | `/prompts/{prompt_id}` | Delete a prompt version |

### 📐 Dimensions (`/dimensions`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/projects/{project_id}/dimensions` | Configure evaluation dimensions |
| `GET` | `/projects/{project_id}/dimensions` | List dimensions for a project |
| `PUT` | `/dimensions/{dimension_id}` | Update dimension description |
| `DELETE` | `/dimensions/{dimension_id}` | Delete an evaluation dimension |

### ⚡ Evaluations (`/evaluations`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/evaluations/run` | Execute live evaluation for an agent |
| `GET` | `/evaluations/{tracking_id}` | Retrieve evaluation output by ID |
| `GET` | `/agents/{agent_id}/evaluations` | List historical evaluations for an agent |
| `GET` | `/agents/{agent_id}/evaluations/latest` | Retrieve latest evaluation result |

---

## 📂 Repository Structure

```text
agent_evaluation_system/
├── app/                      # FastAPI backend application
│   ├── api/                  # API route handlers & endpoints
│   ├── core/                 # App configurations & settings
│   ├── db/                   # Database connection & queries
│   ├── models/               # Pydantic schemas & data models
│   ├── services/             # LLM evaluation & LangChain workflows
│   └── main.py               # Application entry point
├── docker/                   # Docker configurations & database init scripts
│   └── postgres/init.sql     # Database tables initialization
├── frontend/                 # React + Vite frontend application
│   ├── src/
│   │   ├── api.js            # Frontend API client
│   │   ├── App.jsx           # Main application view & router
│   │   ├── main.jsx          # React DOM entry
│   │   └── styles.css        # Responsive styling
│   ├── index.html            # Vite HTML template
│   ├── package.json          # Node dependencies and scripts
│   ├── vite.config.js        # Vite configuration & dev proxy
│   └── README.md             # Frontend-specific documentation
├── docker-compose.yml        # Docker Compose configuration for PostgreSQL
├── requirements.txt          # Python dependencies
├── .env                      # Backend environment variables
└── README.md                 # Project root documentation
```

---

## 📄 License

This project is licensed for development and educational use.
