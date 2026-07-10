from app.db.connection import get_db_connection

def create_new_agent(agent_name: str, project_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            INSERT INTO agent (agent_name, project_id)
            VALUES (%s, %s)
            RETURNING *
            """,
            (agent_name, project_id)
        )

        created_agent = cur.fetchone()
        conn.commit()
        return created_agent

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to create agent: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_agent_by_id(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT * FROM agent
            WHERE agent_id = %s
            """,
            (agent_id,)
        )

        return cur.fetchone()

    except Exception as e:
        raise Exception(f"Failed to fetch agent: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_agents_by_project_id(project_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM agent
            WHERE project_id = %s
            ORDER BY agent_id
            """,
            (project_id,)
        )

        return cur.fetchall()

    except Exception as e:
        raise Exception(f"Failed to fetch agents: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def update_agent_name(agent_id: int, agent_name: str):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            UPDATE agent
            SET agent_name = %s
            WHERE agent_id = %s
            RETURNING *
            """,
            (agent_name, agent_id)
        )

        updated_agent = cur.fetchone()
        conn.commit()
        return updated_agent

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to update agent: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def delete_agent_by_id(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            DELETE FROM agent
            WHERE agent_id = %s
            RETURNING *
            """,
            (agent_id,)
        )

        deleted_agent = cur.fetchone()
        conn.commit()
        return deleted_agent

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to delete agent: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_project_id_by_agent_id(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")

        cur.execute(
            """
            SELECT project_id
            FROM agent
            WHERE agent_id = %s
            """,
            (agent_id,)
        )

        result = cur.fetchone()

        if result is None:
            raise Exception(f"No agent found with agent_id: {agent_id}")

        return result[0]

    except Exception as e:
        raise Exception(f"Failed to fetch project_id for agent_id {agent_id}: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()