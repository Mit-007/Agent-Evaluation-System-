from pydantic import BaseModel
from typing import TypedDict

class Dimension_schema(TypedDict):
    dimension_name : str
    dimension_description : str

class SetDimensions(BaseModel):
    dimensions_list : list[Dimension_schema]