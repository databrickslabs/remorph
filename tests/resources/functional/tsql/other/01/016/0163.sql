-- tsql sql:
CREATE TABLE #temp_table
(
    id INT,
    totalprice DECIMAL(10, 2),
    discount DECIMAL(10, 2)
);

WITH temp_data AS
(
    SELECT 1 AS id, 10.5 AS totalprice, 0.1 AS discount
)
INSERT INTO #temp_table (id, totalprice, discount)
SELECT id, totalprice, discount
FROM temp_data;

ALTER TABLE #temp_table
ADD total_revenue AS (CAST(totalprice AS DECIMAL(10, 2)) * (1 - discount));

SELECT * FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;
