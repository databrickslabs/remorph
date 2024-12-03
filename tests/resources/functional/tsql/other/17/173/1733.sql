--Query type: DML
DECLARE @g geography;
SET @g = geography::STGeomFromText('LINESTRING(0 0, 0 1, 1 0)', 4326);
SELECT @g.AsGml();
-- REMORPH CLEANUP: DROP VARIABLE @g;
