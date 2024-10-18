--Query type: DDL
SELECT c_custkey, c_name, c_address
INTO #temp
FROM (
    VALUES (1, 'Customer1', 'Address1'),
           (2, 'Customer2', 'Address2')
) AS temp (c_custkey, c_name, c_address);

ALTER TABLE #temp
ALTER COLUMN c_custkey DROP MASKED;

SELECT *
FROM #temp;
-- REMORPH CLEANUP: DROP TABLE #temp;