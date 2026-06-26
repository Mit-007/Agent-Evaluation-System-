from app.db.connection import cur,conn

def create_dimension_result(tracking_id: int,dimension_id: int,score: int):
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

def get_result_by_id(
    result_id: int
):
    ...

def get_results_by_tracking_id(
    tracking_id: int
):
    ...

def get_result_by_dimension(
    tracking_id: int,
    dimension_id: int
):
    ...

def update_dimension_score(
    result_id: int,
    score: int
):
    ...

def delete_result(
    result_id: int
):
    ...