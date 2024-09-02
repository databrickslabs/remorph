--Query type: DQL
DECLARE @g GEOMETRY = 'Point(2 2 2 2)';
WITH temp_result AS (
    SELECT @g AS geom
)
SELECT geom.HasZ
FROM temp_result