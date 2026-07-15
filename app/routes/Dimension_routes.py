from fastapi import APIRouter, HTTPException
from app.db.repositories import dimension_repository as DR
from app.db.repositories import project_dimension_repository as PDR
from app.models.dimension_routes_model import SetDimensions,UpdateDimensions

router = APIRouter(prefix="", tags=["Dimensions Routes"])

@router.post("/projects/{project_id}/dimensions")
def set_dimensions(project_id: int, payload: SetDimensions):
    """
    set a list of dimensions for given project.
    """
    try:
        new_dimensions = DR.create_dimensions_bulk(payload.dimensions_list)
        id_list = []
        for dim in new_dimensions:
            id_list.append(dim[0])
        PDR.assign_dimensions_to_project_in_bulk(project_id,id_list)
        return {
            "message": "Set all dimensions for the given project.",
            "list_of_all_project_dimensions": new_dimensions
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/projects/{project_id}/dimensions")
def view_project_dimensions(project_id: int):
    try:
        result = PDR.get_dimensions_by_project_id(project_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No dimensions found for project with ID {project_id}."
            )

        return result

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.put("/dimensions/{dimension_id}")
def update_project_dimensions(dimension_id: int,payload : UpdateDimensions):
    try:
        result = DR.update_dimension_description(dimension_id,payload.new_dimension_description)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No dimensions found with ID : {dimension_id}."
            )

        return {
            "dimension_id" : result[0],
            "dimension_name" : result [1],
            "dimension_description" : result[2]
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@router.delete("/dimensions/{dimension_id}")
def delete_project_dimensions(dimension_id: int):
    try:
        result = DR.delete_dimension(dimension_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No dimensions found with ID : {dimension_id}."
            )

        return {
            "dimension_id" : result[0],
            "dimension_name" : result [1],
            "dimension_description" : result[2]
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))