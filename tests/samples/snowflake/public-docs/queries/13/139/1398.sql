-- see https://docs.snowflake.com/en/sql-reference/functions/st_x

SELECT ST_X(ST_MAKEPOINT(37.5, 45.5)), ST_Y(ST_MAKEPOINT(37.5, 45.5));