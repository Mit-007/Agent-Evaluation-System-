from langgraph.types import Send
from app.core.logger import logger
from app.agent.utils.state import *
from app.services.llm_services import get_llm
from app.services.prompt_evalAgent import *

def orchestrator(state: AgentState) -> AgentState:
    logger.info("Node: orchestrator")

    if not state.prompt:
        raise ValueError("Received an empty prompt.")

    if not state.chat:
        raise ValueError("Received an empty chat.")

    if not state.dimensions:
        raise ValueError("Received an empty dimensions list.")

    try:
        llm = get_llm()
    
        if llm is None:
            raise ConnectionError("LLM service is unavailable.")
    
        orchestrator_prompt = prompt_orchestrator(state.prompt, state.chat)
        structured_llm = llm.with_structured_output(OrchestratorResponse)
        result = structured_llm.invoke(orchestrator_prompt)
        
    except TimeoutError as e:
        raise TimeoutError("LLM request timed out.") from e
    
    except ConnectionError as e:
        raise ConnectionError(e) from e
    
    except Exception as e:
        raise RuntimeError("Failed to invoke LLM.") from e

    if not result.is_prompt_valid:
        raise ValueError("Invalid prompt.")

    if not result.is_chat_valid:
        raise ValueError("Invalid chat.")

    return {}


def route_worker(state: AgentState):
    logger.info("Node: route_worker")

    if not state.prompt:
        raise ValueError("Prompt cannot be empty.")

    if not state.chat:
        raise ValueError("Chat cannot be empty.")

    if not state.dimensions:
        logger.warning("No valid dimensions provided.")
        return []

    try:
        return [
            Send(
                "worker",
                WorkerState(
                    prompt=state.prompt,
                    chat=state.chat,
                    dimension=dimension,
                ),
            )
            for dimension in state.dimensions
        ]

    except Exception as e:
        logger.exception("Error while creating worker tasks.")
        raise RuntimeError("Failed to route workers.") from e


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
            raise ConnectionError("LLM service is not available.")
        
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

def aggregator(state: AgentState) -> AgentState:
    """
    Receive all worker outputs and generate the final evaluation summary.
    """
    logger.info("Node: aggregator")

    if not state.prompt:
        raise ValueError("Prompt cannot be empty.")

    if not state.chat:
        raise ValueError("Chat cannot be empty.")

    if not state.worker_output:
        raise ValueError("Worker output is empty.")
    
    try:
        llm = get_llm()

        if llm is None:
            raise ConnectionError("LLM service is unavailable.")

        aggregator_prompt = prompt_aggregator(state.worker_output)
        structured_llm = llm.with_structured_output(AggregatorResponse)
        result = structured_llm.invoke(aggregator_prompt)

        return {
            "response": result.aggregator_llm_response
        }

    except TimeoutError as e:
        raise TimeoutError("Aggregator request timed out.") from e

    except ConnectionError as e:
        raise ConnectionError(e) from e

    except Exception as e:
        logger.exception("Aggregator node failed.")
        raise RuntimeError("Failed to generate evaluation summary.") from e