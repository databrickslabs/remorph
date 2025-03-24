--- Requests

WITH requests AS (
    SELECT *, CURRENT_TIMESTAMP AS extract_ts
    FROM SYS.DM_PDW_EXEC_REQUESTS
    WHERE start_time IS NOT NULL
      AND command IS NOT NULL
      AND end_time > '2000-01-01'
),
     requests_ext AS (
         SELECT *,
                CASE
                    WHEN UPPER(PARSENAME(command, 1)) = 'SELECT' THEN 'QUERY'
                    WHEN UPPER(PARSENAME(command, 1)) = 'WITH' THEN 'QUERY'
                    WHEN UPPER(PARSENAME(command, 1)) IN ('INSERT', 'UPDATE', 'MERGE', 'DELETE', 'TRUNCATE', 'COPY', 'IF', 'BEGIN', 'DECLARE', 'BUILDREPLICATEDTABLECACHE') THEN 'DML'
                    WHEN UPPER(PARSENAME(command, 1)) IN ('CREATE', 'DROP', 'ALTER') THEN 'DDL'
                    WHEN UPPER(PARSENAME(command, 1)) IN ('EXEC', 'EXECUTE') THEN 'ROUTINE'
                    WHEN UPPER(PARSENAME(command, 1)) = 'BEGIN' AND UPPER(PARSENAME(command, 2)) IN ('TRAN', 'TRANSACTION') THEN 'TRANSACTION_CONTROL'
                    WHEN UPPER(PARSENAME(command, 1)) = 'END' AND UPPER(PARSENAME(command, 2)) IN ('TRAN', 'TRANSACTION') THEN 'TRANSACTION_CONTROL'
                    WHEN UPPER(PARSENAME(command, 1)) = 'COMMIT' THEN 'TRANSACTION_CONTROL'
                    WHEN UPPER(PARSENAME(command, 1)) = 'ROLLBACK' THEN 'TRANSACTION_CONTROL'
                    ELSE 'OTHER'
                    END AS command_type
         FROM REQUESTS
     )
SELECT *,
       CASE WHEN @redact_sql_text = 1 THEN '[REDACTED]' ELSE command END AS command
FROM requests_ext;
