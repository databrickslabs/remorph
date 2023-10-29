-- see https://docs.snowflake.com/en/sql-reference/functions/st_geometryfromwkb

-- Set the geometry output format to EWKT
ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT ST_GEOMETRYFROMEWKB('010100000066666666A9CB17411F85EBC19E325641');