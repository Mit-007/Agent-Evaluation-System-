-- =====================================
-- Project Table
-- =====================================

CREATE TABLE IF NOT EXISTS project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- Agent Table
-- =====================================

CREATE TABLE IF NOT EXISTS agent (
    agent_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,

    project_id INTEGER NOT NULL,

    CONSTRAINT fk_agent_project
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
        ON DELETE CASCADE
);


-- =====================================
-- Dimension Table
-- =====================================

CREATE TABLE IF NOT EXISTS dimension (
    dimension_id SERIAL PRIMARY KEY,

    dimension_name VARCHAR(100) NOT NULL,

    dimension_description TEXT NOT NULL
);


-- =====================================
-- Project-Dimension Mapping Table
-- =====================================

CREATE TABLE IF NOT EXISTS project_dimensions (
    project_dimensions_id SERIAL PRIMARY KEY,

    project_id INTEGER NOT NULL,

    dimension_id INTEGER NOT NULL,

    CONSTRAINT fk_project_dimensions_project
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_project_dimensions_dimension
        FOREIGN KEY (dimension_id)
        REFERENCES dimension(dimension_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_project_dimension
        UNIQUE(project_id, dimension_id)
);


-- =====================================
-- prompt Table
-- =====================================

CREATE TABLE IF NOT EXISTS prompt (
    prompt_id SERIAL PRIMARY KEY,

    agent_id INTEGER NOT NULL,

    prompt TEXT NOT NULL,

    version INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT fk_prompt_agent
        FOREIGN KEY (agent_id)
        REFERENCES agent(agent_id)
        ON DELETE CASCADE
);


-- =====================================
-- evaluation_tracking Table
-- =====================================

CREATE TABLE IF NOT EXISTS evaluation_tracking (
    tracking_id SERIAL PRIMARY KEY,

    agent_id INTEGER NOT NULL,

    prompt_id INTEGER NOT NULL,

    input_chat TEXT NOT NULL,

    output_response JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tracking_agent
        FOREIGN KEY (agent_id)
        REFERENCES agent(agent_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tracking_prompt
        FOREIGN KEY (prompt_id)
        REFERENCES prompt(prompt_id)
        ON DELETE CASCADE
);


-- =====================================
-- dimension_results Table
-- =====================================

CREATE TABLE IF NOT EXISTS dimension_results (
    result_id SERIAL PRIMARY KEY,

    tracking_id INTEGER NOT NULL,

    dimension_id INTEGER NOT NULL,

    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 10),

    CONSTRAINT fk_result_tracking
        FOREIGN KEY (tracking_id)
        REFERENCES evaluation_tracking(tracking_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_result_dimension
        FOREIGN KEY (dimension_id)
        REFERENCES dimension(dimension_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_tracking_dimension
        UNIQUE (tracking_id, dimension_id)
);