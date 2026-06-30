from fastapi import APIRouter, HTTPException
from app.db.repositories.prompt_repository import *
from app.models.prompt_routes_model import *

router = APIRouter(prefix="", tags=["Prompt Routes"])


@router.post("/agents/{agent_id}/prompts")
def create_prompt(agent_id: int, payload: PromptCreate):
    try:
        result = create_new_prompt(agent_id, payload.prompt)
        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/prompts")
def view_all_prompt(agent_id: int):
    try:
        result = get_prompts_by_agent_id(agent_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"No prompts found for agent with ID {agent_id}."
            )

        return {
            "columns": ["Prompt_ID", "Agent_ID", "Prompt", "Version"],
            "rows": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/prompts/latest")
def view_last_updated_prompt(agent_id: int):
    try:
        result = get_latest_prompt(agent_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"No prompts found for agent with ID {agent_id}."
            )

        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prompts/{prompt_id}")
def view_prompt(prompt_id: int):
    try:
        result = get_prompt_by_id(prompt_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Prompt with ID {prompt_id} not found."
            )

        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: int, payload: PromptUpdate):
    try:
        result = update_prompt_by_id(prompt_id, payload.new_prompt)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {prompt_id} not found."
            )

        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/prompts/{prompt_id}")
def delete_agent(prompt_id: int):
    try:
        result = delete_prompt_by_id(prompt_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {prompt_id} not found."
            )

        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))