--Query type: DQL
DECLARE @s geometry;
SELECT @s = geometry::STGeomFromText('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0),(2 2, 2 1, 1 1, 1 2, 2 2))', 0)
FROM (
    VALUES (1)
) AS cte(n);
SELECT @s.STInteriorRingN(1).ToString();
