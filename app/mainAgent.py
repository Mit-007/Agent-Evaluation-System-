from app.agent.agent import EvalAgent
from app.core.logger import logger
from tests.data.fake_data_function import *
import uuid

data = {
    "prompt" : get_prompt(),
    "chat" : get_chat(),
    "dimensions" : ["Instruction adherence","Hallucination detection","Tool usage correctness","Missing information detection","Policy violations","Conversation quality"],
    "worker_output" : [],
    "response" : ""
}

logger.info("Start the Graph")

config = {"configurable": {"thread_id": str(uuid.uuid4())}}

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

print("\n\n------------------")
print("|✅ response :-  |")
print("------------------")

draft = result['response']
print(draft)

print("\n\n-----------------------------------")
print("|✅ Deatailed evalution result :- |")
print("-----------------------------------")

for out in result['worker_output']:
    print(f"\n---{out.dimension}")
    print(out.benchmarkScore)
    print("Reason : ",out.worker_llm_response['reason'])
    print("chat issue : ",out.worker_llm_response['chat_issue'])
    print("prompt issue : ",out.worker_llm_response['prompt_issue'])
    print("recommended_prompt_improvements : ",out.worker_llm_response['recommended_prompt_improvements'])

logger.info("End of Graph")
