from app.db.connection import cur,conn

def create_new_agent(agent_name: str,project_id: int):
    cur.execute("INSERT INTO agent (agent_name, project_id)VALUES (%s, %s)RETURNING *",(agent_name, project_id))
    crerated_agent = cur.fetchone()
    conn.commit()
    return crerated_agent

def get_agent_by_id(agent_id: int):
    cur.execute("""SELECT * FROM agent WHERE agent_id = %s """,(agent_id,))
    return cur.fetchone()

def get_agents_by_project_id(project_id: int):
    cur.execute("""SELECT * FROM agent WHERE project_id = %s ORDER BY agent_id""",(project_id,))
    return cur.fetchall()

def update_agent_name(agent_id: int,agent_name: str):
    cur.execute("""UPDATE agent SET agent_name = %s WHERE agent_id = %s  RETURNING *""",(agent_name, agent_id))
    updated_agent = cur.fetchone()
    conn.commit()
    return updated_agent

def delete_agent_by_id(agent_id: int):
    cur.execute("""DELETE FROM agent WHERE agent_id = %s """,(agent_id,))
    conn.commit()

# def agent_exists(agent_id: int):
#     ...

# def get_agent_by_name(agent_name: str):
#     ...