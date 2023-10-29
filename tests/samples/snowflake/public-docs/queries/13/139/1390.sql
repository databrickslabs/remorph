-- see https://docs.snowflake.com/en/sql-reference/functions/st_simplify

SELECT ST_SIMPLIFY(
    TO_GEOGRAPHY('LINESTRING(-122.306067 37.55412, -122.32328 37.561801, -122.325879 37.586852)'),
    1000);