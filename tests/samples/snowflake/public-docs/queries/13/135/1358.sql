-- see https://docs.snowflake.com/en/sql-reference/functions/st_distance

SELECT ST_DISTANCE(ST_MAKEPOINT(0, 0), ST_MAKEPOINT(NULL, NULL));