# Agent Evaluation System — Frontend

A modern, responsive React web interface for managing, configuring, and evaluating AI agents against customizable evaluation criteria.

---

## 🛠️ Tech Stack & Purpose

| Technology | Purpose & Why It's Used |
| :--- | :--- |
| **React** | Core UI library used to build a modular, state-driven interface with reactive component updates for real-time evaluation runs and workspace management. |
| **Vite** | Next-generation frontend build tool providing lightning-fast development server startup, Hot Module Replacement (HMR), and optimized production builds. |
| **@vitejs/plugin-react** | Vite plugin enabling Fast Refresh and seamless JSX/React support. |
| **Lucide React** | Clean, lightweight SVG icon library used for consistent visual navigation, buttons, status indicators, and modal actions. |
| **Custom CSS (Vanilla)** | Pure CSS with modern CSS variables, Flexbox, Grid, and media queries for high performance, smooth animations, and zero framework overhead. |
| **Native Fetch API & Vite Proxy** | Standard asynchronous HTTP client integrated with Vite's proxy configuration to communicate directly with the FastAPI backend without CORS conflicts. |

---

## 🚀 Step-by-Step Setup & Running Guide

### 1. Prerequisites
- **Node.js**: `v18.0.0` or higher ([Download Node.js](https://nodejs.org/))
- **npm**: `v9.0.0` or higher (bundled with Node.js)
- **Backend API**: The FastAPI backend should be running (default: `http://127.0.0.1:8000`).

---

### 2. Navigate to Frontend Directory
Open your terminal in the repository root and switch to the frontend folder:
```powershell
cd frontend
```

---

### 3. Environment Configuration
Create a `.env` file inside the `frontend` folder (or copy from `.env.example`):
```env
VITE_API_BASE_URL=/api
```
> *In development, Vite proxies `/api` requests to `http://127.0.0.1:8000` automatically.*

---

### 4. Install Dependencies
Install the required packages:
```powershell
npm install
```

---

### 5. Start the Development Server
Run the local Vite server:
```powershell
npm run dev
```

---

### 6. Access the Application
Open your browser and navigate to:
```text
http://localhost:5173
```

---

## 🖥️ How to Operate the System (User Guide)

The frontend provides an intuitive end-to-end workflow to manage and evaluate your AI agents:

```
[Create Project] ➔ [Add Agent] ➔ [Add System Prompt] ➔ [Set Dimensions] ➔ [Run Evaluation]
```

### Step 1: Create or Select a Project
- On the **Home** page or **Projects** tab, click **"New project"**.
- Enter a name (e.g., *Customer Support AI*) to group related agents and evaluation criteria.

### Step 2: Add an Agent
- Use the **Project** dropdown to select your project.
- Click **"Add agent"** and provide an agent name (e.g., *Refund Policy Assistant*).

### Step 3: Define the System Prompt
- In the **Agent Setup** card, click **"Add system prompt"** (or **"Create new prompt version"**).
- Define the behavior, tone, constraints, and instructions for the agent.
- Every new prompt is automatically versioned (`v1`, `v2`, etc.).

### Step 4: Configure Evaluation Dimensions
- In the **Quality Bar** section or **Dimensions** tab, click **"Manage"** / **"Add criteria"**.
- Add scoring criteria (e.g., *Accuracy*, *Tone*, *Clarity*) along with descriptions of what a good response looks like.

### Step 5: Run an Evaluation
- In the **"Run an evaluation"** section:
  1. Type a test user message in the input box (e.g., *"How do I return a damaged item?"*).
  2. Click **"Run evaluation"**.
- The system sends the prompt and message to the evaluation pipeline.

### Step 6: Review Results & History
- **Live Output**: Inspect the overall score (out of 10), qualitative assessment summary, and individual dimension breakdown.
- **Evaluation History**: Scroll down to view previous evaluation runs with timestamps and summaries.

---

## 📁 Available Management Pages (Sidebar)

- **Home**: Main dashboard for running test evaluations and viewing live metrics.
- **Projects**: View, rename, or delete existing evaluation projects.
- **Agents**: Browse and manage agents under selected projects.
- **Prompts**: Inspect prompt version history and create new iterations.
- **Dimensions**: Add, update, or remove evaluation benchmarks and scoring criteria.

---

## 📦 Build for Production

To create an optimized production build:
```powershell
npm run build
```
The output will be generated inside the `dist/` directory, ready to be served by any static web server or reverse proxy.
