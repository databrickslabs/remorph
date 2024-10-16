--Query type: DDL
SELECT * INTO #T2 FROM (VALUES (CAST(10.5 AS decimal(10, 2)), 'Hello'), (CAST(20.7 AS decimal(10, 2)), 'World')) AS T2 (column_3, column_4);