
-- snowflake sql:
SELECT
                CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00'::timestamp_ntz)
                AS conv;

-- databricks sql:
SELECT CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00') AS conv;
