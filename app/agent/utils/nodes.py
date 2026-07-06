from langgraph.types import Send
from app.core.logger import logger
from app.agent.utils.state import *
from app.services.llm_services import get_llm
from app.services.prompt_evalAgent import *

def orchestrator(state : AgentState) -> AgentState:
    """ 
    Input Validation using llm: 
    -> check given prompt -if not valid then give "False"
    -> check given chat -if not valid then give "False"
    """
    logger.info("Node:orchestrator")
    try :
        if not state.prompt :
            raise ValueError("Recieve a Empty prompt")

        if not state.chat : 
            raise ValueError("Recieve a Empty chat")
        
        if len(state.dimensions) == 0 :
            raise ValueError("Provide Empty Dimensions List")

        llm = get_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

        orchestrator_prompt = prompt_orchestrator(state.prompt,state.chat)
        structured_llm = llm.with_structured_output(OrchestratorResponse)
        result = structured_llm.invoke(orchestrator_prompt)

        if not result.is_prompt_valid:
            raise ValueError("Provided Prompt are not Valid Prompt")
        
        if not result.is_chat_valid:
            raise ValueError("Provided chat are not Valid chat")

        return {}

    except Exception as e:
        logger.error(f"error found in orchestrator node : {e}")
        return {
            'prompt' : "",
            'chat' : "",
            'dimensions' : [],
            'response' : f"Error Found , {e}"
        }


def route_worker(state : AgentState):
    """
    Route to a worker node using the send() API.
    route to worker for every single dimension.
    """
    logger.info("Node:-route_workers")
    try:
        if not state.prompt or not state.chat :
            raise ValueError("Recieve a Invalid Inputs")

        dimensions = state.dimensions

        if not dimensions or len(dimensions)==0:
            logger.warning("Not a Provide any Valid Dimensions")
            return []

        return [
            Send(
                "worker",
                WorkerState(
                    prompt = state.prompt,
                    chat = state.chat,
                    dimension = dimension
                )
            )
            for dimension in dimensions
        ]

    except Exception as e:
        logger.error(f"error found in route_worker node : {e}")
        return [
            Send(
                "worker",
                WorkerState(
                    prompt="",
                    chat="",
                    dimension={
                        "dimension_name": "",
                        "dimension_description": ""
                    }                   
                )
            )
        ]

def worker(state : WorkerState) -> AgentState:
    """
    perform a evaluation every single dimension base and return evalution result list.
    """
    logger.info("Node:worker")
    try :
        if state.prompt == "" or state.chat == "" :
            raise ValueError("Recieve a Invalid Inputs")

        llm = get_llm()
        
        if not llm:
            raise ValueError("LLM service is not available.")
        
        worker_prompt = prompt_worker(state.prompt,state.chat,state.dimension['dimension_name'],state.dimension["dimension_description"])
        structured_llm = llm.with_structured_output(WorkerResponse)
        result = structured_llm.invoke(worker_prompt)

        # -> if llm change a in dimenssion name then , replce with original 
        result.dimension = state.dimension['dimension_name']

        return {
            "worker_output" : [result]
        }

    except Exception as e:
        logger.error(f"Error in worker_DB_researcher: {e}")
        worker_result = WorkerLlmResponseDict(
            reason=f"Worker execution failed: {str(e)}",
            chat_issue=[],
            prompt_issue=[],
            recommended_prompt_improvements=""
        )
        result = WorkerResponse (
            dimension = state.dimension['dimension_name'],
            worker_llm_response = worker_result,
            benchmarkScore = 0 
        )
        return{
            "worker_output" : [result]
        }

def aggregator(state : AgentState) -> AgentState:
    """
    recive all worker output and make full evalution response draft.
    """
    logger.info("Node:aggregator")
    try :
        if not state.prompt or not state.chat :
            raise ValueError(f"{state.response}")

        if len(state.worker_output)==0:
            raise ValueError("Worker List is empty")
        
        llm = get_llm()

        if not llm:
            raise ValueError("LLM service is not available.")

        aggregator_prompt = prompt_aggregator(state.worker_output)
        structured_llm = llm.with_structured_output(AggregatorResponse)
        result = structured_llm.invoke(aggregator_prompt)

        return {
            'response' : result.aggregator_llm_response
        }
    except Exception as e:
        logger.error(f"Error in Aggregator node : {e}")

        return {
            'response' : f"{e}"
        }