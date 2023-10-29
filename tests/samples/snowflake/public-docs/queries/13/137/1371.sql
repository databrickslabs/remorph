-- see https://docs.snowflake.com/en/sql-reference/functions/st_intersects

SELECT ST_INTERSECTS(
    TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
    TO_GEOGRAPHY('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))')
    );