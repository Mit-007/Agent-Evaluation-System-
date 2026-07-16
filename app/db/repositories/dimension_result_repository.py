from app.db.connection import get_db_connection,release_db_connection
from psycopg2.extras import execute_values

def create_dimension_results_bulk(dimension_results_list):
    conn = cur = None
    try:
        conn, cur = get_db_connection()

        query = """
            INSERT INTO dimension_results (
                tracking_id,
                dimension_id,
                score
            )
            VALUES %s
            RETURNING *;
        """

        values = [
            (
                result["tracking_id"],
                result["dimension_id"],
                result["score"]
            )
            for result in dimension_results_list
        ]

        if not values:
            return []

        execute_values(cur, query, values)

        inserted_dimension_results = cur.fetchall()

        conn.commit()

        return inserted_dimension_results

    except ConnectionError:
        raise

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Failed to create dimension results: {e}")

    finally:
        if conn:
            release_db_connection(conn, cur)