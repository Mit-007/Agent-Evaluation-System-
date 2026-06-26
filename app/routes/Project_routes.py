from fastapi import APIRouter 
from app.db.repositories.project_repository import *
from app.models.project_routes_model import *

router = APIRouter(prefix="", tags=["Project Routers"])

@router.post("/projects")
def create_new_project(payload : ProjectCreate):
    return create_project(payload.project_name)

@router.get("/projects")
def view_all_project():
    result = list_projects()
    return result

@router.get("/projects/{project_id}")
def view_project(project_id : int):
    result = get_project_by_id(project_id)
    return result