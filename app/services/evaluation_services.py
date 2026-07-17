from app.db.repositories.prompt_repository import get_latest_prompt
from app.db.repositories.project_dimension_repository import get_dimensions_by_project_id
from app.db.repositories.evaluation_tracking_repository import create_evaluation_tracking
from app.db.repositories.dimension_result_repository import create_dimension_results_bulk
from app.agent.agent import EvalAgent
from app.core.logger import logger
import json
import uuid

def performe_evalution(project_id: int, agent_id: int, chat: str):
    """
    Perform an evaluation of the given agent, based on the chat and prompt.
    First, fetch the prompt and dimensions from the database.
    Run the evaluation_agent and retrieve the results.
    Store the evaluation result in the tracking table and each dimension's result in the evaluation_result table.
    divide into three part : 1) data collect for evaluation from database 
                                -> collect latest prompt version from "Prompt" table
                                -> get dimension list for current project "Project_Dimensions" jion "Dimension" Table.
                                -> make "dim_dict" dict those mapping dimension name with id, those use for add data into database after evaluation
                                -> "dim_list" contains all dimensions with description , pass into agent input state
                             2) run the graph and get result
                             3) store evalution result in database
                                -> given respone by agent is pydantic object , convert into json and then store "Evaluation_Tracking" table
                                -> store each dimension score in "Dimension_Result" Table  
    """
    try:
        # ============
        # part 1 : data retrive from database :
        # ============
        prompt_data = get_latest_prompt(agent_id)

        if prompt_data is None:
            raise ValueError(f"No prompt found for agent_id={agent_id}")

        dimensions = get_dimensions_by_project_id(project_id)

        if not dimensions:
            raise ValueError(f"No dimensions found for project_id={project_id}")

        #  --> list of dimension with description for graph input 
        dim_list = []

        #  --> store { "dimension_name" : "dimension_id" }, for store output data in DB (store each dimenstion result using ID)
        dim_dict = {}

        for dim in dimensions:
            dimension_detail = {
                "dimension_name" : dim[1],
                "dimension_description" : dim[2]
            }
            dim_list.append(dimension_detail)
            dim_dict[dim[1]] = dim[0]

        data = {
            #  --> extraxt prompt from tuple 
            "prompt": prompt_data[2],
            "chat": chat,
            "dimensions": dim_list,
            "worker_output": [],
            "response": ""
        }
        

        
        # ============
        # part 2 : Run The Graph  :
        # ============
        logger.info("Starting Evaluation Graph")

        config = { "configurable": {"thread_id": str(uuid.uuid4())} }
        result = EvalAgent.invoke(data, config)

        logger.info("Evaluation Graph Completed")



        # ============
        # part 3 : Manage a graph result and store in database:
        # ============

        # --> indicate the Average score 
        overall_score = 0

        # --> list of all worker output convert into json from pydantic model
        dimensions_result = []

        for worker in result["worker_output"]:
            overall_score += worker.benchmarkScore
            dimensions_result.append(worker.model_dump())

        overall_score = overall_score / len(result["worker_output"]) if len(result["worker_output"]) > 0 else 0

        #  --> dict for store result in db, before store convert into json
        output_response = {
            "score": overall_score,
            "overall_assessment_summary": result["response"],
            "dimensions_result": dimensions_result,
        }
        json_output = json.dumps(output_response)

        # --> store full evaluation result into DB(Table : evaluation_tracking)
        tracking_data = create_evaluation_tracking(agent_id,prompt_data[0],chat,json_output)

        #  --> list of benchmark score of dimensions
        benchmark_scores = []
        dimension_results = []

        for output in result["worker_output"]:
            if output.dimension == '' or output.dimension not in dim_dict:
                continue 

            dimension_results.append({
                "tracking_id": tracking_data[0],
                "dimension_id": dim_dict[output.dimension],
                "score": output.benchmarkScore,
            })

            benchmark_scores.append(
                {
                    "dimension": output.dimension,
                    "score": output.benchmarkScore
                }
            )
        
        #  --> store single dimension result in DB(Table : dimension_results) 
        if dimension_results:
            create_dimension_results_bulk(dimension_results)

        return {
            "benchmark_score": benchmark_scores,
            "response": result["response"],
            "dimensions_results" : result['worker_output'],
            "overall_score": overall_score
        }

    except (ValueError, ConnectionError,TimeoutError,RuntimeError):
        logger.error("Evaluation validation failed.")
        raise

    except Exception as e:
        logger.error("Unexpected error while performing evaluation.")
        raise RuntimeError("Failed to perform evaluation. {e}") from e