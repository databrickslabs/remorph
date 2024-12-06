-- tsql sql:
SELECT id, a1, a2 * 10 AS a2 FROM (VALUES (1, 'value1', NULL), (2, 'value2', NULL)) AS TempTable(id, a1, a2);
