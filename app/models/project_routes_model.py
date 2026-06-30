from pydantic import BaseModel

class ProjectCreate(BaseModel):
    project_name: str

class ProjectNameUpdate(BaseModel):
    project_new_name: str