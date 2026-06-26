from pydantic import BaseModel

class AgentCreate(BaseModel):
    agent_name: str

class AgentNameUpdate(BaseModel):
    agent_new_name: str
