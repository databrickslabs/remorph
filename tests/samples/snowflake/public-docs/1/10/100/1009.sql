CREATE or replace TABLE extreme_point_collection (id INTEGER, g GEOGRAPHY);
INSERT INTO extreme_point_collection (id, g)
    SELECT column1, TO_GEOGRAPHY(column2) FROM VALUES
        (1, 'POINT(-180 0)'),
        (2, 'POINT(180 0)'),
        (3, 'LINESTRING(-179 0, 179 0)'),
        (4, 'LINESTRING(-60 30, 60 30)'),
        (5, 'LINESTRING(-60 -30, 60 -30)');