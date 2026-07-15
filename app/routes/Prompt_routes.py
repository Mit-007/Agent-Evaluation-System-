from fastapi import APIRouter, HTTPException
from app.db.repositories import prompt_repository as PR
from app.models import prompt_routes_model as PM

router = APIRouter(prefix="", tags=["Prompt Routes"])


@router.post("/agents/{agent_id}/prompts")
def create_prompt(agent_id: int, payload: PM.PromptCreate):
    try:
        result = PR.create_new_prompt(agent_id, payload.prompt)
        return {
            "prompt_id" : result[0],
            "agent_id" : result[1],
            "prompt" : result[2],
            "version" : result[3]
        }

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/prompts")
def view_all_prompt(agent_id: int):
    try:
        result = PR.get_prompts_by_agent_id(agent_id)

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

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/prompts/latest")
def view_last_updated_prompt(agent_id: int):
    try:
        result = PR.get_latest_prompt(agent_id)

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

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prompts/{prompt_id}")
def view_prompt(prompt_id: int):
    try:
        result = PR.get_prompt_by_id(prompt_id)

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

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: int, payload: PM.PromptUpdate):
    try:
        result = PR.update_prompt_by_id(prompt_id, payload.new_prompt)

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

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/prompts/{prompt_id}")
def delete_agent(prompt_id: int):
    try:
        result = PR.delete_prompt_by_id(prompt_id)

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

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))