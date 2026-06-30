from fastapi import APIRouter, HTTPException
from app.models.evaluation_model import EvaluationRun
from app.services.evaluation_services import performe_evalution
from app.db.repositories.evaluation_tracking_repository import *
from app.db.repositories.agent_repository import get_project_id_by_agent_id

router = APIRouter(prefix="", tags=["Evaluation Routes"])


@router.post("/evaluations/run")
def run_new_evaluation(payload: EvaluationRun):
    try:
        project_id = get_project_id_by_agent_id(payload.agent_id)
        result = performe_evalution(project_id,payload.agent_id,payload.chat)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/evaluations/{tracking_id}")
def view_evaluation_result(tracking_id: int):
    try:
        result = get_tracking_by_id(tracking_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Evaluation with tracking ID {tracking_id} not found."
            )

        return {
            "tracking_id" : result[0],
            "agent_id" : result[1],
            "prompt_id" : result[2],
            "chat" : result[3],
            "output_response" : result[4],
            "timestamp" : result[5]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/agents/{agent_id}/evaluations")
def view_agent_evaluation_result(agent_id: int):
    try:
        result = get_tracking_by_agent_id(agent_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No evaluation records found for agent with ID {agent_id}."
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.get("/agents/{agent_id}/evaluations/latest")
def view_agent_latest_evaluation_result(agent_id: int):
    try:
        result = get_latest_tracking(agent_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No evaluation records found for agent with ID {agent_id}."
            )

        return {
            "tracking_id" : result[0],
            "agent_id" : result[1],
            "prompt_id" : result[2],
            "chat" : result[3],
            "output_response" : result[4],
            "timestamp" : result[5]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )