from fastapi import APIRouter, HTTPException
from app.db.repositories.agent_repository import *
from app.models.agent_routes_model import *

router = APIRouter(prefix="", tags=["Agent Routes"])


@router.post("/projects/{project_id}/agents")
def create_agent(project_id: int, payload: AgentCreate):
    try:
        result = create_new_agent(payload.agent_name, project_id)

        return {
            "agent_id": result[0],
            "agent_name": result[1],
            "project_id": result[2]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/agents")
def view_all_agent(project_id: int):
    try:
        result = get_agents_by_project_id(project_id)

        return {
            "columns": ["Agent_ID", "Agent_Name", "Project_ID"],
            "rows": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}")
def view_agent(agent_id: int):
    try:
        result = get_agent_by_id(agent_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {agent_id} not found."
            )

        return {
            "agent_id": result[0],
            "agent_name": result[1],
            "project_id": result[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/agents/{agent_id}")
def update_agent(agent_id: int, payload: AgentNameUpdate):
    try:
        result = update_agent_name(agent_id, payload.agent_new_name)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {agent_id} not found."
            )

        return {
            "agent_id": result[0],
            "agent_name": result[1],
            "project_id": result[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int):
    try:
        result = delete_agent_by_id(agent_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {agent_id} not found."
            )

        return {
            "agent_id": result[0],
            "agent_name": result[1],
            "project_id": result[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))