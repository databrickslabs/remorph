--Query type: DQL
DECLARE @customer geometry;
DECLARE @supplier geometry;

SET @customer = geometry::STGeomFromText('LINESTRING(0 2, 2 0, 4 2)', 0);
SET @supplier = geometry::STGeomFromText('POINT(5 5)', 0);

WITH temp_result AS (
    SELECT @customer.STRelate(@supplier, 'FF*FF****') AS Relation
)
SELECT * FROM temp_result;
