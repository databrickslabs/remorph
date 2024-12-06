-- tsql sql:
WITH indexes AS (
    SELECT object_id, name
    FROM (
        VALUES (1, 'idx1'),
               (2, 'idx2')
    ) AS t(object_id, name)
),
 tables AS (
    SELECT object_id, name
    FROM (
        VALUES (1, 'table1'),
               (2, 'table2')
    ) AS t(object_id, name)
)
SELECT i.object_id, i.name, t.object_id, t.name
FROM indexes i
INNER JOIN tables t ON i.object_id = t.object_id
WHERE i.name = 'idx1' AND t.name = 'table1';
