-- tsql sql:
DECLARE @g1 geometry = 'CIRCULARSTRING(0 0, 1 2.1082, 3 6.3246, 0 7, -3 6.3246, -1 2.1082, 0 0)';
DECLARE @g2 geometry = 'LINESTRING(0 5, 7 10, 3 7)';
WITH cte AS (
    SELECT @g1 AS geom1, @g2 AS geom2
)
SELECT geom1.ShortestLineTo(geom2).ToString()
FROM cte;
