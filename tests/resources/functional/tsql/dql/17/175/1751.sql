--Query type: DQL
DECLARE @geom geometry;
SET @geom = geometry::STGeomFromText('POINT(10 20 30 40)', 0);
WITH temp_result AS (
    SELECT @geom AS geom
)
SELECT geom.STAsText() AS text, geom.AsTextZM() AS text_zm
FROM temp_result;
