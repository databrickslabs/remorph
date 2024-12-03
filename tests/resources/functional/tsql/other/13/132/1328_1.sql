--Query type: DML
INSERT INTO sample (id, geom)
SELECT id, geom
FROM (
    VALUES
        (0, geometry::Point(0, 0, 0)),
        (1, geometry::Point(0, 1, 0)),
        (2, geometry::Point(0, 2, 0)),
        (3, geometry::Point(0, 3, 0)),
        (4, geometry::Point(0, 4, 0))
) AS temp (id, geom);
