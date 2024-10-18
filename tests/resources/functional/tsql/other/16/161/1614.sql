--Query type: DML
CREATE TABLE #GeographyData
(
    id INT,
    geo GEOGRAPHY
);

INSERT INTO #GeographyData (id, geo)
VALUES
    (1, GEOGRAPHY::STGeomFromText('LINESTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653)', 4326)),
    (2, GEOGRAPHY::STGeomFromText('LINESTRING(-122.358 47.653, -122.348 47.649, -122.348 47.658, -122.358 47.658, -122.358 47.653)', 4326));

WITH BufferedGeography AS
(
    SELECT id, geo.BufferWithCurves(1e-20) AS buffered_geo
    FROM #GeographyData
)

SELECT id, buffered_geo.ToString() AS buffered_geo_string
FROM BufferedGeography;

DROP TABLE #GeographyData;