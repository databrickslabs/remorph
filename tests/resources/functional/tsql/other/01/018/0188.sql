--Query type: DDL
CREATE TABLE #temp_table
(
    customer_id INT,
    name VARCHAR(255),
    new_column VARCHAR(255) UNIQUE
);

INSERT INTO #temp_table (customer_id, name, new_column)
SELECT customer_id, name, CAST('' AS VARCHAR(255)) AS new_column
FROM (
    SELECT customer_id, name
    FROM customer
) AS temp_table;

SELECT * FROM #temp_table;
-- REMORPH CLEANUP: DROP TABLE #temp_table;