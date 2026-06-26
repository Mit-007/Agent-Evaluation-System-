from app.db.connection import cur , conn

def get_latest_prompt(agent_id: int):
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

def get_latest_prompt_version(agent_id: int):
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

def get_prompt_count(agent_id: int):
    cur.execute(
        """
        SELECT COUNT(*) AS prompt_count
        FROM prompt
        WHERE agent_id = %s;
        """,
        (agent_id,)
    )

    result = cur.fetchone()
    return result["prompt_count"]

def create_new_prompt(agent_id: int,prompt: str):
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

def get_prompts_by_agent_id(agent_id: int):
    cur.execute(
        """ 
        SELECT *
        FROM prompt
        WHERE agent_id = %s;
        """,
        (agent_id,)
    )
    result = cur.fetchone()
    return result

def get_prompt_by_id(prompt_id: int):
    cur.execute(
        """
        SELECT *
        FROM prompt
        WHERE prompt_id = %s;
        """,
        (prompt_id,)
    )

    return cur.fetchone()

def update_prompt(prompt_id: int,prompt: str):
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


def delete_prompt(prompt_id: int):
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