-- see https://docs.snowflake.com/en/sql-reference/functions/st_npoints

CREATE OR REPLACE TABLE geometry_shapes (g GEOMETRY);
INSERT INTO geometry_shapes VALUES
    ('POINT(66 12)'),
    ('MULTIPOINT((45 21), (12 54))'),
    ('LINESTRING(40 60, 50 50, 60 40)'),
    ('MULTILINESTRING((1 1, 32 17), (33 12, 73 49, 87.1 6.1))'),
    ('POLYGON((17 17, 17 30, 30 30, 30 17, 17 17))'),
    ('MULTIPOLYGON(((-10 0,0 10,10 0,-10 0)),((-10 40,10 40,0 20,-10 40)))'),
    ('GEOMETRYCOLLECTION(POLYGON((-10 0,0 10,10 0,-10 0)),LINESTRING(40 60, 50 50, 60 40), POINT(99 11))')
    ;

SELECT ST_NPOINTS(g), ST_ASWKT(g) FROM geometry_shapes;