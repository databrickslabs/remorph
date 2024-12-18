-- tsql sql:
DECLARE @p geometry;
SET @p = geometry::STGeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', 0);
SELECT @p.STIsClosed() AS result
FROM (VALUES (1)) AS cte(id);
