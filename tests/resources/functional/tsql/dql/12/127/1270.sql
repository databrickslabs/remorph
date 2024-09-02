--Query type: DQL
SELECT CAST(10.5 AS DECIMAL(10, 2)) AS MyDecimalColumn, CAST(20.7 AS NUMERIC(10, 2)) AS MyNumericColumn FROM (VALUES (1)) AS MyTable(MyTableID);