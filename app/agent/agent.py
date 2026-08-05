from app.agent.utils.state import AgentState
from app.agent.utils import nodes
from langgraph.graph import StateGraph ,START ,END
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(AgentState)

builder.add_node("orchestrator",nodes.orchestrator)
builder.add_node("worker",nodes.worker)
builder.add_node("aggregator",nodes.aggregator)

builder.add_edge(START,"orchestrator")
builder.add_conditional_edges("orchestrator",nodes.route_worker,["worker"])
builder.add_edge("worker","aggregator")
builder.add_edge("aggregator",END)

EvalAgent = builder.compile(checkpointer=InMemorySaver())