--Query type: DQL
WITH indexes AS (
  SELECT 1 AS object_id, 'Index1' AS name, 'CLUSTERED' AS type_desc
  UNION ALL
  SELECT 2 AS object_id, 'Index2' AS name, 'NONCLUSTERED' AS type_desc
),
tables AS (
  SELECT 1 AS object_id, 'MyFactTable' AS name
  UNION ALL
  SELECT 2 AS object_id, 'MyDimTable' AS name
)
SELECT i.object_id, i.name, t.object_id, t.name
FROM indexes i
INNER JOIN tables t ON i.object_id = t.object_id
WHERE i.type_desc = 'CLUSTERED'
AND t.name = 'MyFactTable';
