from app.db.repositories.prompt_repository import get_latest_prompt
from app.db.repositories.project_dimension_repository import get_dimensions_by_project_id
from app.db.repositories.evaluation_tracking_repository import create_evaluation_tracking
from app.db.repositories.dimension_result_repository import create_dimension_result
from app.agent.agent import EvalAgent
from app.core.logger import logger
import json
import uuid

def performe_evalution(project_id: int, agent_id: int, chat: str):
    """
    Perform an evaluation of the given agent based on the chat and prompt.
    First, fetch the prompt and dimensions from the database.
    Run the evaluation agent and retrieve the results.
    Store the evaluation result in the tracking table and each dimension's result in the evaluation_result table.
    """
    try:
        prompt_data = get_latest_prompt(agent_id)

        if prompt_data is None:
            raise Exception(f"No prompt found for agent_id={agent_id}")

        dimensions = get_dimensions_by_project_id(project_id)

        if not dimensions:
            raise Exception(f"No dimensions found for project_id={project_id}")

        dim_list = []
        dim_dict = {}

        for dim in dimensions:
            dim_list.append(dim[1])
            dim_dict[dim[1]] = dim[0]

        data = {
            "prompt": prompt_data[2],
            "chat": chat,
            "dimensions": dim_list,
            "worker_output": [],
            "response": ""
        }

        logger.info("Starting Evaluation Graph")

        config = { "configurable": {"thread_id": str(uuid.uuid4())} }

        result = EvalAgent.invoke(data, config)

        logger.info("Evaluation Graph Completed")

        overall_score = sum(
            output.benchmarkScore
            for output in result["worker_output"]
        )

        output_response = {
            "score": overall_score,
            "overall_assessment_summary": result["response"],
            "dimensions_result": [
                worker.model_dump() for worker in result["worker_output"]
            ]
        }

        json_output = json.dumps(output_response)

        tracking_data = create_evaluation_tracking(agent_id,prompt_data[0],chat,json_output)

        benchmark_scores = []

        for output in result["worker_output"]:
            create_dimension_result(
                tracking_data[0],
                dim_dict[output.dimension],
                output.benchmarkScore
            )

            benchmark_scores.append(
                {
                    "dimension": output.dimension,
                    "score": output.benchmarkScore
                }
            )

        return {
            "benchmark_score": benchmark_scores,
            "response": result["response"],
            "dimensions_results" : result['worker_output'],
            "overall_score": overall_score
        }

    except Exception as e:
        logger.exception("Evaluation failed")
        return {
            "error" : f"Failed to perform evaluation: {e}"
        }