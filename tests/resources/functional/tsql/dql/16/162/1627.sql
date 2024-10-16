--Query type: DQL
DECLARE @g geography;
SELECT geography::Point(30.0, 20.0, 4326).STConvexHull() AS convex_hull
FROM (
    VALUES ('abcdefg')
) AS l (l_shipinstruct);