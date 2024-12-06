-- tsql sql:
CREATE TABLE #temp_result (id INT, product_name VARCHAR(50));
INSERT INTO #temp_result (id, product_name)
VALUES
    (1, 'Product A'),
    (2, 'Product B'),
    (3, 'Product C');
UPDATE STATISTICS #temp_result (id, product_name);
SELECT *
FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
