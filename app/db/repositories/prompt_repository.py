from app.db.connection import get_db_connection,release_db_connection

def get_latest_prompt(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM prompt
            WHERE agent_id = %s
            ORDER BY version DESC
            LIMIT 1;
            """,
            (agent_id,)
        )
        return cur.fetchone()

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        raise Exception(f"Failed to fetch latest prompt: {e}")

    finally:
        release_db_connection(conn, cur)

def get_latest_prompt_version(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT version
            FROM prompt
            WHERE agent_id = %s
            ORDER BY version DESC
            LIMIT 1;
            """,
            (agent_id,)
        )
        result = cur.fetchone()

        if result is None:
            return 0
        
        return result[0]

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        raise Exception(f"Failed to fetch latest prompt version: {e}")

    finally:
        release_db_connection(conn, cur)


def get_prompt_count(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT COUNT(*) AS prompt_count
            FROM prompt
            WHERE agent_id = %s;
            """,
            (agent_id,)
        )

        result = cur.fetchone()
        return result[0]

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        raise Exception(f"Failed to fetch prompt count: {e}")

    finally:
        release_db_connection(conn, cur)


def create_new_prompt(agent_id: int, prompt: str):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        version = get_latest_prompt_version(agent_id) + 1

        cur.execute(
            """
            INSERT INTO prompt (
                agent_id,
                prompt,
                version
            )
            VALUES (%s, %s, %s)
            RETURNING *;
            """,
            (agent_id, prompt, version)
        )

        new_prompt = cur.fetchone()
        conn.commit()

        return new_prompt

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to create prompt: {e}")

    finally:
        release_db_connection(conn, cur)

def get_prompts_by_agent_id(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM prompt
            WHERE agent_id = %s
            ORDER BY version DESC;
            """,
            (agent_id,)
        )

        return cur.fetchall()

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        raise Exception(f"Failed to fetch prompts: {e}")

    finally:
        release_db_connection(conn, cur)


def get_prompt_by_id(prompt_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM prompt
            WHERE prompt_id = %s;
            """,
            (prompt_id,)
        )

        return cur.fetchone()

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        raise Exception(f"Failed to fetch prompt: {e}")

    finally:
        release_db_connection(conn, cur)


def update_prompt_by_id(prompt_id: int, prompt: str):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            UPDATE prompt
            SET prompt = %s
            WHERE prompt_id = %s
            RETURNING *;
            """,
            (prompt, prompt_id)
        )

        updated_prompt = cur.fetchone()
        conn.commit()

        return updated_prompt

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to update prompt: {e}")

    finally:
        release_db_connection(conn, cur)


def delete_prompt_by_id(prompt_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise ConnectionError("Unable to connect to the database.")
        
        cur.execute(
            """
            DELETE FROM prompt
            WHERE prompt_id = %s
            RETURNING *;
            """,
            (prompt_id,)
        )

        deleted_prompt = cur.fetchone()
        conn.commit()

        return deleted_prompt

    except ConnectionError as e:
        raise ConnectionError(e)

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to delete prompt: {e}")

    finally:
        release_db_connection(conn, cur)