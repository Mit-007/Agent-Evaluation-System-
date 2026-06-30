from pydantic import BaseModel

class EvaluationRun(BaseModel):
    agent_id : int
    chat : str