from fastapi import APIRouter 
from app.models.evaluation_model import EvaluationRun
from app.services.evaluation_services import performe_evalution
from app.db.repositories.evaluation_tracking_repository import *

router = APIRouter(prefix="", tags=["Evaluation Routers"])

@router.post("/evaluations/run")
def run_new_evaluation(payload : EvaluationRun):
    result = performe_evalution(payload.project_id, payload.agent_id, payload.chat)
    return result

@router.get("/evaluations/{tracking_id}")
def view_evaluation_result(tracking_id : int):
    result = get_tracking_by_id(tracking_id)
    return result

@router.get("/agents/{agent_id}/evaluations")
def view_agent_evaluation_result(agent_id : int):
    result = get_tracking_by_agent_id(agent_id)
    return result