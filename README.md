# AI Agent Evaluation Platform

An AI Agent Management and Evaluation Platform built with **FastAPI**, **Streamlit**, **LangChain**, and **LangGraph**. The platform allows users to organize AI agents inside projects, manage prompts, configure evaluation dimensions, and track agent performance through evaluations.

---

# Project Overview

This project provides a centralized workspace to build and evaluate AI agents.

### Features

- Create and manage multiple projects
- Create and manage AI agents inside each project
- Create, update, and organize prompts for every agent
- Configure custom evaluation dimensions for projects
- Run evaluations on AI agents
- View latest evaluation history for agents

---

# Project Workflow

```text
Create Project
       │
       ▼
Create AI Agents
       │
       ▼
Create Prompts
       │
       ▼
Setup Evaluation Dimensions
       │
       ▼
Run Agent Evaluation
       │
       ▼
View & Track Evaluation Results
```

---

# Technologies Used

| Layer | Technology |
|--------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Framework | LangChain |
| Workflow | LangGraph |
| Database | PostgreSQL |
| Server | Uvicorn |
| Container | Docker & Docker Compose |

---

# Project Setup

## 1. Install PostgreSQL using Docker Compose

Make sure **Docker Desktop / Docker Engine** is running.

Start PostgreSQL using the provided compose file.

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker ps
```

---

## 2. Configure Environment Variables

Create a `.env` file and update the following values.

```env
# ===========
# Database Setup
# ===========
HOST=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
PORT=5432

# ===========
# Gemini API Key
# ===========
GOOGLE_API_KEY="your_api_key"
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

### Step 1

Start Docker Engine (PostgreSQL).

```bash
docker compose up -d
```

### Step 2

Start the FastAPI backend.

```bash
uvicorn app.main:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

### Step 3

Run the Streamlit frontend.

```bash
streamlit run frontend/main_page.py
```

---

# API Endpoints

## Project Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/projects` | View all projects |
| POST | `/projects` | Create new project |
| GET | `/projects/{project_id}` | View project |
| PUT | `/projects/{project_id}` | Update project |
| DELETE | `/projects/{project_id}` | Delete project |

---

## Agent Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/projects/{project_id}/agents` | Create agent |
| GET | `/projects/{project_id}/agents` | View all agents |
| GET | `/agents/{agent_id}` | View agent |
| PUT | `/agents/{agent_id}` | Update agent |
| DELETE | `/agents/{agent_id}` | Delete agent |

---

## Dimension Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/projects/{project_id}/dimensions` | Set dimensions |
| GET | `/projects/{project_id}/dimensions` | View dimensions |

---

## Prompt Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/agents/{agent_id}/prompts` | Create prompt |
| GET | `/agents/{agent_id}/prompts` | View prompts |
| GET | `/agents/{agent_id}/prompts/latest` | Latest prompt |
| GET | `/prompts/{prompt_id}` | View prompt |
| PUT | `/prompts/{prompt_id}` | Update prompt |
| DELETE | `/prompts/{prompt_id}` | Delete prompt |

---

## Evaluation Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/evaluations/run` | Run evaluation |
| GET | `/evaluations/{tracking_id}` | Evaluation result |
| GET | `/agents/{agent_id}/evaluations` | Agent evaluations |
| GET | `/agents/{agent_id}/evaluations/latest` | Latest evaluation |


---

# Future Improvements

- Authentication & Authorization
- Agent versioning
- Evaluation dashboard
- Track and compare evaluation results
- Export evaluation reports
- Multi-model support
---

# License

This project is intended for educational and development purposes.