--Query type: DQL
DECLARE @h geography = 'POLYGON((30.533 48.566, -15.283 48.1, -20.3 49.45, 30.533 48.566))';
SELECT @h.STConvexHull().ToString() AS convex_hull
FROM (VALUES (1)) AS temp_table(column_name);