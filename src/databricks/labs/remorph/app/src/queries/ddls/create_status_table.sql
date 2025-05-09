CREATE TABLE IF NOT EXISTS {RECON_JOB_RUN_DETAILS_TABLE_NAME}
(
    job_run_id
    BIGINT
    PRIMARY
    KEY,
    start_time
    TIMESTAMP,
    end_time
    TIMESTAMP,
    user_name
    STRING,
    duration
    BIGINT, -- Store duration in seconds
    source_dialect
    STRING,
    workspace_id
    STRING,
    workspace_name
    STRING,
    status
    STRING,
    exception_message
    STRING,
    created_at
    TIMESTAMP,
    updated_at
    TIMESTAMP
) USING DELTA;