from app.agent.agent import EvalAgent
from app.core.logger import logger
from tests.data.fake_data_function import *

data = {
    "prompt" : get_prompt(),
    "chat" : get_chat(),
    "dimensions" : ["Instruction adherence","Hallucination detection","Tool usage correctness","Missing information detection","Policy violations","Conversation quality"],
    "worker_output" : [],
    "response" : ""
}

logger.info("Start the Graph")

config = {"configurable": {"thread_id": "thread-1"}}

result = EvalAgent.invoke(data,config)

print("\n\n----------------")
print("|✅ prompt :-  |")
print("----------------")

print(result['prompt'])

print("\n\n--------------")
print("|✅ chat :-  |")
print("--------------")

print(result['chat'])

print("\n\n--------------------")
print("|✅ dimensions :-  |")
print("--------------------")

print(result['dimensions'])

print("\n\n-----------------------")
print("|✅ Worker_output :-  |")
print("-----------------------")

for out in result['worker_output']:
    print(f"\n---{out.dimension}")
    print(out.worker_llm_response)
    print(out.benchmarkScore)

print("\n\n------------------")
print("|✅ response :-  |")
print("------------------")

print(result['response'])

logger.info("End of Graph")
