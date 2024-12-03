--Query type: DDL
CREATE TABLE sales (id INT, name VARCHAR(50));
INSERT INTO sales (id, name)
VALUES (1, 'a'), (2, 'b');

WITH sales_mv AS (
    SELECT id, name
    FROM sales
)
SELECT id, name
INTO #sales_mv
FROM sales_mv;

CREATE UNIQUE CLUSTERED INDEX idx_sales_mv
ON #sales_mv (id);

SELECT *
FROM #sales_mv;

-- REMORPH CLEANUP: DROP TABLE #sales_mv;
-- REMORPH CLEANUP: DROP TABLE sales;
