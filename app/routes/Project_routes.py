from fastapi import APIRouter , HTTPException
from app.db.repositories.project_repository import *
from app.models.project_routes_model import *

router = APIRouter(prefix="", tags=["Project Routes"])

@router.post("/projects")
def create_new_project(payload: ProjectCreate):
    try:
        result = create_project(payload.project_name)

        return {
            "project_id": result[0],
            "project_name": result[1],
            "created_at": result[2]
        }

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects")
def view_all_project():
    try:
        result = list_projects()

        return {
            "columns": ["Project_ID", "Project_Name", "Status"],
            "rows": result
        }

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/projects/{project_id}")
def view_project(project_id: int):
    try:
        result = get_project_by_id(project_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Project with ID {project_id} not found."
            )

        return {
            "project_id": result[0],
            "project_name": result[1],
            "created_at": result[2]
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/projects/{project_id}")
def update_project(project_id: int, payload: ProjectNameUpdate):
    try:
        result = update_project_name(project_id, payload.project_new_name)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {project_id} not found."
            )

        return {
            "project_id": result[0],
            "project_name": result[1],
            "created_at": result[2]
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/projects/{project_id}")
def delete_project(project_id: int):
    try:
        result = delete_project_by_id(project_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent with ID {project_id} not found."
            )

        return {
            "project_id": result[0],
            "project_name": result[1],
            "created_at": result[2]
        }

    except HTTPException:
        raise

    except ConnectionError as e:
        raise HTTPException(status_code=503,detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))