from pydantic import BaseModel

class ProjectCreate(BaseModel):
    project_name: str