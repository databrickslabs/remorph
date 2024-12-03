--Query type: DML
DECLARE @g geography;
SET @g = geography::STGeomFromText('POINT(-122.34900 47.65100)', 4326);
SELECT result
FROM (
    VALUES (@g.BufferWithTolerance(1, .5, 0).ToString())
) AS temp_result(result);
