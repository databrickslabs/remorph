-- tsql sql:
SELECT SUM(value) AS TotalSum
FROM (
    VALUES (10), (20), (30)
) AS TemporaryResultSet(value);
