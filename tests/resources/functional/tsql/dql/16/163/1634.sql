-- tsql sql:
DECLARE @region geography;
DECLARE @route geography;
SET @region = geography::STGeomFromText('POLYGON((-71.088 42.315, -71.078 42.311, -71.078 42.320, -71.088 42.320, -71.088 42.315))', 4326);
SET @route = geography::STGeomFromText('LINESTRING(-71.090 42.318, -71.073 42.318)', 4326);
WITH temp_result AS (
    SELECT @region.STIntersection(@route).ToString() AS result
)
SELECT * FROM temp_result;
