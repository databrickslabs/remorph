--Query type: DQL
WITH cte AS (SELECT geometry::Parse('LINESTRING(2 4, 6 6, 5 4, 2 4)') AS g)
SELECT g.STCurveToLine().STGeometryType()
FROM cte