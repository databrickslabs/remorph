--Query type: DQL
WITH OrderedPoints AS (
    SELECT x, y, line, seq,
    ROW_NUMBER() OVER (PARTITION BY line ORDER BY seq) AS row_num
    FROM (
        VALUES (0, 2, 1, 1),
               (1, 1, 1, 2),
               (2, 2, 1, 3),
               (1, 1, 2, 1),
               (1, 0, 2, 2)
    ) AS Points (x, y, line, seq)
)
SELECT 
    line,
    geometry::STGeomFromText('LINESTRING(' + 
    (SELECT STRING_AGG(CONVERT(VARCHAR(10), x) + ' ' + CONVERT(VARCHAR(10), y), ', ') 
     FROM OrderedPoints AS p2
     WHERE p2.line = p1.line) + ')', 0).STAsText() AS LineString
FROM OrderedPoints AS p1
GROUP BY line;