from app.db.connection import cur,conn

def create_project(project_name: str):
    cur.execute("INSERT INTO project (project_name) VALUES (%s) RETURNING *",(project_name,))
    new_project = cur.fetchone()
    conn.commit()
    return new_project

def get_project_by_id(project_id: int):
    cur.execute("SELECT * FROM project WHERE project_id = %s", (project_id,))
    return cur.fetchone()

def list_projects():
    cur.execute("SELECT * FROM project ORDER BY created_at DESC")
    return cur.fetchall()

# def get_project_by_name(project_name: str):
#     ...
  
# def update_project_name(project_id: int, project_name: str):
#     ...

# def delete_project(project_id: int):
#     ...

# def project_exists(project_id: int):
#     ...