
-- snowflake sql:
SELECT
                CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00'::timestamp_ntz);

-- databricks sql:
SELECT CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', CAST('2019-01-01 00:00:00 +03:00' AS TIMESTAMP_NTZ));
