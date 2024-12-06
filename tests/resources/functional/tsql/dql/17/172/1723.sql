-- tsql sql:
DECLARE @customer geometry;
DECLARE @supplier geometry;
SET @customer = geometry::STGeomFromText('LINESTRING(0 2, 2 0, 4 2)', 0);
SET @supplier = geometry::STGeomFromText('POINT(1 1)', 0);
WITH temp AS (
    SELECT @customer.STTouches(@supplier) AS touches
)
SELECT * FROM temp;
