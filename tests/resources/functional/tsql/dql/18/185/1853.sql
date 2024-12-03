--Query type: DQL
DECLARE @g GEOMETRY = 'Polygon((1 1, 3 3, 3 1, 1 3, 1 1))';
WITH cte AS (
    SELECT @g AS geom
)
SELECT geom.IsValidDetailed()
FROM cte
