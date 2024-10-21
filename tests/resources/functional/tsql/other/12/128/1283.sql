--Query type: DDL
CREATE TABLE #T2 (c3 INT, c4 VARCHAR(10));
INSERT INTO #T2
SELECT *
FROM (VALUES (1, 'value1'), (2, 'value2')) AS temp (c3, c4);