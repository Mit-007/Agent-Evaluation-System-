from app.agent.utils.state import AgentState
from app.agent.utils.nodes import *
from langgraph.graph import StateGraph ,START ,END
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(AgentState)

builder.add_node("orchestrator",orchestrator)
builder.add_node("worker",worker)
builder.add_node("aggregator",aggregator)

builder.add_edge(START,"orchestrator")
builder.add_conditional_edges("orchestrator",route_worker,["worker"])
builder.add_edge("worker","aggregator")
builder.add_edge("aggregator",END)

EvalAgent = builder.compile(checkpointer=InMemorySaver())