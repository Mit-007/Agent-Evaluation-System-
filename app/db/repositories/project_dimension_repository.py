from app.db.connection import get_db_connection,release_db_connection
from psycopg2.extras import execute_values

def assign_dimensions_to_project_in_bulk(project_id: int, dimension_ids: list[int]):
    conn = None
    cur = None

    try:
        conn, cur = get_db_connection()

        query = """
            INSERT INTO project_dimensions (
                project_id,
                dimension_id
            )
            VALUES %s
            RETURNING *;
        """

        values = [
            (project_id, dimension_id)
            for dimension_id in dimension_ids
        ]

        execute_values(
            cur,
            query,
            values
        )

        result = cur.fetchall()

        conn.commit()

        return result

    except Exception as e:
        if conn:
            conn.rollback()

        raise Exception(f"Failed to assign dimensions to project: {e}")

    finally:
        release_db_connection(conn, cur)
    
def assign_dimension_to_project(project_id: int, dimension_id: int):
    try:
        conn, cur = get_db_connection()
        
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
                dimension_id
            )
        )

        result = cur.fetchone()
        conn.commit()
        return result

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to assign dimension to project: {e}")

    finally:
        release_db_connection(conn, cur)


def get_dimensions_by_project_id(project_id: int):
    try:
        conn, cur = get_db_connection()
        
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

    except Exception as e:
        raise Exception(f"Failed to fetch project dimensions: {e}")

    finally:
        release_db_connection(conn, cur)