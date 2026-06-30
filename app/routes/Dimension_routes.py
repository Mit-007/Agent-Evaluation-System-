from fastapi import APIRouter, HTTPException
from app.db.repositories.dimension_repository import *
from app.db.repositories.project_dimension_repository import *
from app.models.dimension_routes_model import SetDimensions

router = APIRouter(prefix="", tags=["Dimensions Routes"])

@router.post("/projects/{project_id}/dimensions")
def set_dimensions(project_id: int, payload: SetDimensions):
    """
    set a list of dimensions for given project.
    """
    try:
        for dim_data in payload.dimensions_list:
            new_dimension = create_new_dimension(dim_data["dimension_name"],dim_data["dimension_description"])
            assign_dimension_to_project(project_id , new_dimension[0])

        result = get_dimensions_by_project_id(project_id)

        return {
            "message": "Set all dimensions for the given project.",
            "list_of_all_project_dimensions": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/projects/{project_id}/dimensions")
def view_project_dimensions(project_id: int):
    try:
        result = get_dimensions_by_project_id(project_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No dimensions found for project with ID {project_id}."
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )