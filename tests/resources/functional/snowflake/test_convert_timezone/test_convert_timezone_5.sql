
-- source:
SELECT
                CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00'::timestamp_ntz);

-- databricks_sql:
SELECT CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00');
