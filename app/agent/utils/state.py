from typing import Annotated
from pydantic import BaseModel
import operator

# ===========
# LLm response Schema 
# ===========
class OrchestratorResponse(BaseModel):
    is_prompt_valid : bool
    is_chat_valid : bool
    updated_dimensions : list[str]

class WorkerResponse(BaseModel):
    dimension : str
    worker_llm_response : str
    benchmarkScore : int 

class AggregatorResponse(BaseModel):
    aggregator_llm_response : str


# ===========
# Worker State
# ===========
class WorkerState(BaseModel):
    prompt : str
    chat : str
    dimension : str


# ============
# Main Agent State
# ============
class AgentState(BaseModel):
    prompt : str
    chat : str
    dimensions : list[str]
    worker_output : Annotated[list[WorkerResponse],operator.add]
    response : str