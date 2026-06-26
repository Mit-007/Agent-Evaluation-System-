from app.db.connection import cur,conn

def create_new_dimension(dimension_name: str,dimension_description: str,project_id : int):
    cur.execute(
        """
        INSERT INTO dimension (
            dimension_name,
            dimension_description
        )
        VALUES (%s, %s)
        RETURNING *
        """,
        (dimension_name, dimension_description)
    )
    new_dimension = cur.fetchone()
    cur.execute(
        """
        INSERT INTO project_dimensions (
            project_id,
            dimension_id
        )
        VALUES (%s, %s)
        RETURNING *;
        """,
        (
            project_id,
            new_dimension[0]   
        )
    )
    conn.commit()
    return new_dimension

def get_dimensions_by_project_id(project_id: int):
    cur.execute(
        """
        SELECT
            d.dimension_id,
            d.dimension_name,
            d.dimension_description
        FROM project_dimensions pd
        INNER JOIN dimension d
            ON pd.dimension_id = d.dimension_id
        WHERE pd.project_id = %s
        ORDER BY d.dimension_id;
        """,
        (project_id,)
    )

    return cur.fetchall()


def get_dimension_by_id(
    dimension_id: int
):
    ...

def get_dimension_by_name(
    dimension_name: str
):
    ...

def list_dimensions():
    ...

def update_dimension(
    dimension_id: int,
    dimension_name: str,
    dimension_description: str
):
    ...

def delete_dimension(
    dimension_id: int
):
    ...

def dimension_exists(
    dimension_id: int
):
    ...