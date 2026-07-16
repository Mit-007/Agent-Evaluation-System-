from app.db.connection import get_db_connection,release_db_connection

def create_dimension_result(tracking_id: int, dimension_id: int, score: int):
    conn = cur = None
    try:
        conn, cur = get_db_connection()
        
        cur.execute(
            """
            INSERT INTO dimension_results (
                tracking_id,
                dimension_id,
                score
            )
            VALUES (%s, %s, %s)
            RETURNING *;
            """,
            (
                tracking_id,
                dimension_id,
                score
            )
        )

        new_dimension_result = cur.fetchone()
        conn.commit()

        return new_dimension_result

    except ConnectionError:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to create dimension result: {e}")

    finally:
        release_db_connection(conn, cur)