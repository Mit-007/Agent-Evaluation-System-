from app.db.connection import get_db_connection ,release_db_connection


def create_project(project_name: str):
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            "INSERT INTO project (project_name) VALUES (%s) RETURNING *",
            (project_name,)
        )
        project = cur.fetchone()
        conn.commit()
        return project

    except ConnectionError:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to create project: {e}")

    finally:
        release_db_connection(conn, cur)


def get_project_by_id(project_id: int):
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            "SELECT * FROM project WHERE project_id = %s",
            (project_id,)
        )
        return cur.fetchone()

    except ConnectionError:
        raise
    
    except Exception as e:
        raise Exception(f"Failed to fetch project: {e}")

    finally:
        release_db_connection(conn, cur)

def list_projects():
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            "SELECT * FROM project ORDER BY created_at DESC"
        )
        return cur.fetchall()

    except ConnectionError:
        raise
    
    except Exception as e:
        raise Exception(f"Failed to fetch projects: {e}")

    finally:
        release_db_connection(conn, cur)

def update_project_name(project_id: int, project_name: str):
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            """
            UPDATE project
            SET project_name = %s
            WHERE project_id = %s
            RETURNING *
            """,
            (project_name, project_id)
        )

        project = cur.fetchone()
        conn.commit()
        return project

    except ConnectionError:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to update project: {e}")

    finally:
        release_db_connection(conn, cur)


def delete_project_by_id(project_id: int):
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            """
            DELETE FROM project
            WHERE project_id = %s
            RETURNING *
            """,
            (project_id,)
        )

        project = cur.fetchone()
        conn.commit()
        return project

    except ConnectionError:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to delete project: {e}")

    finally:
        release_db_connection(conn, cur)