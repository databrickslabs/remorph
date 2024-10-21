--Query type: DDL
CREATE TABLE #customer_hash (ch VARCHAR(50));
WITH combined_customers AS (
    SELECT ch FROM (VALUES ('customer1'), ('customer2')) AS customers(ch)
    UNION ALL
    SELECT ch FROM (VALUES ('customer3'), ('customer4')) AS customers(ch)
)
INSERT INTO #customer_hash (ch)
SELECT MIN(ch) FROM combined_customers;
SELECT * FROM #customer_hash;
-- REMORPH CLEANUP: DROP TABLE #customer_hash;