def assign_dimension_to_project(
    project_id: int,
    dimension_id: int
):
    ...

def remove_dimension_from_project(
    project_id: int,
    dimension_id: int
):
    ...

def get_dimensions_by_project_id(
    project_id: int
):
    ...

def get_projects_by_dimension_id(
    dimension_id: int
):
    ...

def is_dimension_assigned(
    project_id: int,
    dimension_id: int
):
    ...