-- see https://docs.snowflake.com/en/sql-reference/functions/st_distance

WITH d AS
    ( ST_DISTANCE(ST_MAKEPOINT(0, 0), ST_MAKEPOINT(1, 0)) )
SELECT d / 1000 AS kilometers, d / 1609 AS miles;