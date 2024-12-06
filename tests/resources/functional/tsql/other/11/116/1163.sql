-- tsql sql:
CREATE TABLE #geography_data (id INT, geo geography);
INSERT INTO #geography_data (id, geo)
VALUES (1, geography::Point(10, 20, 4326)),
       (2, geography::Point(30, 40, 4326)),
       (3, geography::Point(50, 60, 4326));
CREATE SPATIAL INDEX SIndx_GeographyData_geo
ON #geography_data(geo)
WITH (GRIDS = (LEVEL_3 = HIGH, LEVEL_2 = HIGH));
SELECT * FROM #geography_data;
-- REMORPH CLEANUP: DROP TABLE #geography_data;
