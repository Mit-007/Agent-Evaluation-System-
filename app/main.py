from fastapi import FastAPI
from app.routes import Dimension_routes, Evaluation_routes, Project_routes, Agent_routes , Prompt_routes

app = FastAPI()

app.include_router(Project_routes.router)
app.include_router(Agent_routes.router)
app.include_router(Dimension_routes.router)
app.include_router(Prompt_routes.router)
app.include_router(Evaluation_routes.router)