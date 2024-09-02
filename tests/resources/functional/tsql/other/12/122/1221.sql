--Query type: DDL
CREATE TABLE SpatialTable
(
    id INT PRIMARY KEY,
    geometry_col GEOMETRY
);

CREATE SPATIAL INDEX SIndx_SpatialTable_geometry_col1
ON SpatialTable(geometry_col)
WITH (
    BOUNDING_BOX = (0, 0, 500, 200)
);

WITH temp_result AS
(
    SELECT 1 AS id, geometry::Point(10, 20, 0) AS geometry_col
    UNION ALL
    SELECT 2 AS id, geometry::Point(30, 40, 0) AS geometry_col
)
INSERT INTO SpatialTable (id, geometry_col)
SELECT * FROM temp_result;