--Query type: DDL
SELECT SUM(value) AS TotalSum
FROM (
    VALUES (10), (20), (30)
) AS TemporaryResultSet(value);