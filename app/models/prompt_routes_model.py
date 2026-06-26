from pydantic import BaseModel

class PromptCreate(BaseModel):
    prompt : str

class PromptUpdate(BaseModel):
    new_prompt : str