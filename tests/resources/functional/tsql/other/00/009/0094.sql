--Query type: DDL
WITH sales AS (
    SELECT *
    FROM (
        VALUES
            (1, '2022-01-01', 100.0),
            (2, '2022-01-02', 200.0)
    ) AS sales (sale_id, sale_date, sale_amount)
)
SELECT *
FROM sales;
