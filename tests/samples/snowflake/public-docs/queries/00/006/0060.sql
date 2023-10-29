-- see https://docs.snowflake.com/en/sql-reference/functions/st_disjoint

-- These two polygons intersect and are not disjoint.
SELECT ST_DISJOINT(
    TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
    TO_GEOGRAPHY('POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))')
    );