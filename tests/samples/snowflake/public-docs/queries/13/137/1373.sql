-- see https://docs.snowflake.com/en/sql-reference/functions/st_length

SELECT ST_LENGTH(TO_GEOGRAPHY('LINESTRING(0.0 0.0, 1.0 0.0)'));