from fastapi import FastAPI
from app.routes import Dimension_routes, Evaluation_routes, Project_routes, Agent_routes , Prompt_routes
from app.db.connection import init_db_pool , close_db_pool

app = FastAPI()

app.include_router(Project_routes.router)
app.include_router(Agent_routes.router)
app.include_router(Dimension_routes.router)
app.include_router(Prompt_routes.router)
app.include_router(Evaluation_routes.router)

@app.on_event("startup")
def startup():
    init_db_pool()

@app.on_event("shutdown")
def shutdown():
    close_db_pool()