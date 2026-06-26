from fastapi import APIRouter 
from app.db.repositories.agent_repository import *
from app.models.agent_routes_model import *

router = APIRouter(prefix="", tags=["Agent Routers"])

@router.post("/projects/{project_id}/agents")
def create_agent(project_id : int,payload :AgentCreate):
    result = create_new_agent(payload.agent_name,project_id)
    return result

@router.get("/projects/{project_id}/agents")
def view_all_agent(project_id : int):
    result = get_agents_by_project_id(project_id)
    return result

@router.get("/agents/{agent_id}")
def view_agent(agent_id : int):
    result = get_agent_by_id(agent_id)
    return result

@router.put("/agents/{agent_id}")
def update_agent(agent_id : int,payload :AgentNameUpdate):
    result = update_agent_name(agent_id,payload.agent_new_name)
    return result

@router.delete("/agents/{agent_id}")
def delete_agent(agent_id : int):
    result = delete_agent_by_id(agent_id)
    return {
        "message" : "You agent deleted Sucessfully"
    }