-- see https://docs.snowflake.com/en/sql-reference/functions/st_buffer

SELECT ST_BUFFER(TO_GEOMETRY('POINT(0 0)'), 1);
