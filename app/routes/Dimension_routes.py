from fastapi import APIRouter 
from app.db.repositories.dimension_repository import *
from app.models.dimension_routes_model import SetDimensions

router = APIRouter(prefix="", tags=["Dimensions Routers"])

@router.post("/projects/{project_id}/dimensions")
def set_dimensions(project_id : int , payload:SetDimensions):
    for dim_data in payload.dimensions_list: 
        create_new_dimension(dim_data['dimension_name'],dim_data['dimension_description'],project_id)

    result =  get_dimensions_by_project_id(project_id)
    return{
        "message" : "set all dimension in given project",
        "list_of_all_project_dimensions" : result
    }

@router.get("/projects/{project_id}/dimensions")
def view_project_dimensions(project_id : int):
    result =  get_dimensions_by_project_id(project_id)
    return result