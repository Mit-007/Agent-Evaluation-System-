# Evaluo frontend

Responsive React dashboard for the existing FastAPI agent-evaluation API. It creates projects, agents, prompts, dimensions, and evaluation runs through the API—no mock data is used.

## Run locally

1. Start the existing backend from the repository root: `uvicorn app.main:app --reload`
2. In this folder run `npm install` then `npm run dev`.
3. Open the Vite URL (usually `http://localhost:5173`). Requests to `/api` are proxied to FastAPI at port 8000.

## Production

Run `npm run build`. Deploy `dist/` behind a web server that routes `/api/*` to the FastAPI service and removes the `/api` prefix. Set `VITE_API_BASE_URL` at build time if your API is served at a different same-origin path.
