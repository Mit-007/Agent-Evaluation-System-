from typing import Annotated , TypedDict
from pydantic import BaseModel
import operator

# ===========
# LLm response Schema 
# ===========

# -> orchestrator llm schema :
class OrchestratorResponse(BaseModel):
    is_prompt_valid : bool
    is_chat_valid : bool

# -> worker node schema :
class ChatIssue(TypedDict):
    evidence: str
    explanation: str

class PromptIssue(TypedDict):
    evidence: str
    explanation: str

class WorkerLlmResponseDict(TypedDict):
    reason : str
    chat_issue : list[ChatIssue]
    prompt_issue : list[PromptIssue]
    recommended_prompt_improvements : str

class WorkerResponse(BaseModel):
    dimension : str
    worker_llm_response : WorkerLlmResponseDict
    benchmarkScore : int 

# -> aggregator Llm schema : 

class AggregatorResponse(BaseModel):
    aggregator_llm_response : str

# ===========
# Dimension Dict :
# ==========

class Dimension(TypedDict):
    dimension_name : str
    dimension_description : str

# ===========
# Worker State
# ===========
class WorkerState(BaseModel):
    prompt : str
    chat : str
    dimension : Dimension

# ============
# Main Agent State
# ============
class AgentState(BaseModel):
    prompt : str
    chat : str
    dimensions : list[Dimension]
    worker_output : Annotated[list[WorkerResponse],operator.add]
    response : str 