from app.db.connection import get_db_connection

def create_new_dimension(dimension_name: str, dimension_description: str):
    try:
        conn, cur = get_db_connection()

        if conn is None or cur is None:
            raise Exception("Unable to connect to the database.")
        
        cur.execute(
            """
            INSERT INTO dimension (
                dimension_name,
                dimension_description
            )
            VALUES (%s, %s)
            RETURNING *;
            """,
            (
                dimension_name,
                dimension_description
            )
        )
        new_dimension = cur.fetchone()
        conn.commit()
        return new_dimension

    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to create dimension: {e}")

    finally:
        cur.close()
        conn.close()