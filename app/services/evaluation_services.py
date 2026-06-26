from app.db.repositories.prompt_repository import get_latest_prompt
from app.db.repositories.dimension_repository import get_dimensions_by_project_id
from app.db.repositories.evaluation_tracking_repository import create_evaluation_tracking
from app.db.repositories.dimension_result_repository import create_dimension_result
from app.agent.agent import EvalAgent
from app.core.logger import logger

def performe_evalution(project_id:int, agent_id:int, chat:str):
    prompt_data = get_latest_prompt(agent_id)
    dimensions = get_dimensions_by_project_id(project_id)
    dim_list = []
    dim_dict = dict()
    for dim in dimensions:
        dim_list.append(dim[1])
        dim_dict[dim[1]] = dim[0]
    data = {
        "prompt" : prompt_data[2],
        "chat" : chat,
        "dimensions" : dim_list,
        "worker_output" : [],
        "response" : ""
    }

    logger.info("Start the Graph")
    config = {"configurable": {"thread_id": "thread-1"}}
    result = EvalAgent.invoke(data,config)
    logger.info("end of graph")

    overall_score = 0
    for out in result['worker_output']:
        overall_score += out.benchmarkScore

    tracking_data = create_evaluation_tracking(agent_id , prompt_data[0] ,chat ,result['response'] ,overall_score)

    benchmarks_scores = []
    for out in result['worker_output']:
        create_dimension_result(tracking_data[0] ,dim_dict[out.dimension] ,out.benchmarkScore)
        ben_dic = {"dimension" : out.dimension , "score":out.benchmarkScore}
        benchmarks_scores.append(ben_dic)

    return {
        "benchmark_score":benchmarks_scores,
        "response" : result['response'],
        "overall_score" : overall_score
    }
