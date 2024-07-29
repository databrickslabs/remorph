
-- presto sql:
SELECT AVG(CAST(json_extract_scalar(CAST(extra AS JSON), '$.satisfaction_rating') AS INT)) FROM dual;

-- databricks sql:
SELECT AVG(CAST(CAST(extra AS STRING):satisfaction_rating AS INT)) FROM dual;
