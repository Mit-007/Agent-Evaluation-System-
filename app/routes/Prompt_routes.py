from fastapi import APIRouter 
from app.db.repositories.prompt_repository import *
from app.models.prompt_routes_model import *

router = APIRouter(prefix="", tags=["Prompt Routers"])

@router.post("/agents/{agent_id}/prompts")
def create_prompt(agent_id : int,payload : PromptCreate):
    result = create_new_prompt(agent_id,payload.prompt)
    return result

@router.get("/agents/{agent_id}/prompts")
def view_all_prompt(agent_id : int):
    result = get_prompts_by_agent_id(agent_id)
    return result

@router.get("/agents/{agent_id}/prompts/latest")
def view_last_updated_prompt(agent_id : int):
    result = get_latest_prompt(agent_id)
    return result

@router.get("/prompts/{prompt_id}")
def view_prompt(prompt_id : int):
    result = get_prompt_by_id(prompt_id)
    return result