from app.db.connection import get_db_connection,release_db_connection

def create_evaluation_tracking(
    agent_id: int,
    prompt_id: int,
    input_chat: str,
    output_response : dict
):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            INSERT INTO evaluation_tracking (
                agent_id,
                prompt_id,
                input_chat,
                output_response
            )
            VALUES (%s, %s, %s, %s)
            RETURNING *;
            """,
            (
                agent_id,
                prompt_id,
                input_chat,
                output_response
            )
        )

        tracking = cur.fetchone()
        conn.commit()
        return tracking

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to create evaluation tracking: {e}")

    finally:
        release_db_connection(conn, cur)


def get_tracking_by_id(tracking_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM evaluation_tracking
            WHERE tracking_id = %s;
            """,
            (tracking_id,)
        )

        return cur.fetchone()

    except Exception as e:
        raise Exception(f"Failed to fetch evaluation tracking: {e}")

    finally:
        release_db_connection(conn, cur)


def get_tracking_by_agent_id(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM evaluation_tracking
            WHERE agent_id = %s
            ORDER BY tracking_id DESC;
            """,
            (agent_id,)
        )

        return cur.fetchall()

    except Exception as e:
        raise Exception(f"Failed to fetch agent evaluation history: {e}")

    finally:
        release_db_connection(conn, cur)


def get_latest_tracking(agent_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            SELECT *
            FROM evaluation_tracking
            WHERE agent_id = %s
            ORDER BY tracking_id DESC
            LIMIT 1;
            """,
            (agent_id,)
        )

        return cur.fetchone()

    except Exception as e:
        raise Exception(f"Failed to fetch latest evaluation tracking: {e}")

    finally:
        release_db_connection(conn, cur)


def delete_tracking(tracking_id: int):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            DELETE FROM evaluation_tracking
            WHERE tracking_id = %s
            RETURNING *;
            """,
            (tracking_id,)
        )

        deleted_tracking = cur.fetchone()
        conn.commit()

        return deleted_tracking

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to delete evaluation tracking: {e}")

    finally:
        release_db_connection(conn, cur)