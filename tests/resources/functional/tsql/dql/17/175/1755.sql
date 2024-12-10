-- tsql sql:
DECLARE @customer geometry;
SET @customer = geometry::STGeomFromText('POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))', 0);
WITH customer AS (
    SELECT @customer AS geom
)
SELECT geom.STIsEmpty()
FROM customer
