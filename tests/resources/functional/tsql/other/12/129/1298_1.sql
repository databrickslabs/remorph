-- tsql sql:
CREATE TABLE #temp_table (customer_key INT, order_key INT);
INSERT INTO #temp_table (customer_key, order_key)
VALUES (1, 2), (3, 4);
ALTER TABLE #temp_table
DROP COLUMN order_key;
SELECT *
FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
