--Query type: DQL
DECLARE @customer geometry;
SET @customer = geometry::STGeomFromText('POLYGON((0 0, 0 10, 5 5, 10 10, 10 0, 0 0))', 0);
WITH customer_convex_hull AS (
    SELECT @customer.STConvexHull().ToString() AS customer_convex_hull
)
SELECT * FROM customer_convex_hull;