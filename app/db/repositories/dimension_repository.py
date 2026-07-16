from app.db.connection import get_db_connection,release_db_connection
from psycopg2.extras import execute_values

def create_dimensions_bulk(dimensions_list):
    conn = cur = None
    try:
        conn, cur = get_db_connection()

        query = """
            INSERT INTO dimension (
                dimension_name,
                dimension_description
            )
            VALUES %s
            RETURNING *;
        """

        values = [
            (
                dim["dimension_name"],
                dim["dimension_description"]
            )
            for dim in dimensions_list
        ]

        execute_values(cur, query, values)

        inserted_dimensions = cur.fetchall()

        conn.commit()

        return inserted_dimensions

    except ConnectionError:
        raise

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to create dimensions: {e}")

    finally:
        if conn:
            release_db_connection(conn, cur)

def update_dimension_description(dimension_id: int, dimension_description: str):
    conn = cur = None
    try:
        conn, cur = get_db_connection()

        cur.execute(
            """
            UPDATE dimension
            SET dimension_description = %s
            WHERE dimension_id = %s
            RETURNING *
            """,
            (dimension_description, dimension_id)
        )

        updated_dimension = cur.fetchone()
        conn.commit()
        return updated_dimension

    except ConnectionError:
        raise

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to update dimension description: {e}")

    finally:
        release_db_connection(conn, cur)

def delete_dimension(dimension_id: int):
    conn = cur = None
    try:
        conn, cur = get_db_connection()

        cur.execute(
            """
            DELETE FROM dimension
            WHERE dimension_id = %s
            RETURNING *
            """,
            (dimension_id,)
        )

        deleted_dimension = cur.fetchone()
        conn.commit()
        return deleted_dimension

    except ConnectionError:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to delete dimension: {e}")

    finally:
        release_db_connection(conn, cur)