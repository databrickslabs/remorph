--Query type: DCL
CREATE TABLE #temp_result (customer_key VARCHAR(50), customer_name VARCHAR(50));
INSERT INTO #temp_result (customer_key, customer_name)
VALUES ('customer_key', 'customer_name');
REVOKE SELECT ON #temp_result TO PUBLIC;
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
