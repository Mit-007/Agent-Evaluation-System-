from app.db.connection import conn,cur

def create_evaluation_tracking(agent_id: int,prompt_id: int,input_chat: str,output_response: str,overall_score: float):
    cur.execute(
        """
        INSERT INTO evaluation_tracking (
            agent_id,
            prompt_id,
            input_chat,
            output_response,
            overall_score
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (
            agent_id,
            prompt_id,
            input_chat,
            output_response,
            overall_score
        )
    )

    tracking = cur.fetchone()
    conn.commit()
    return tracking

def get_tracking_by_id(tracking_id: int):
    cur.execute(
        """
        SELECT *
        FROM evaluation_tracking
        WHERE tracking_id = %s;
        """,
        (tracking_id,)
    )

    return cur.fetchone()

def get_tracking_by_agent_id(agent_id: int):
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

def get_latest_tracking(agent_id: int):
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

def delete_tracking(tracking_id: int):
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