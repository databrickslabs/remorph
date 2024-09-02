--Query type: DDL
WITH Sales AS (
    SELECT *
    FROM (
        VALUES
            (20000101, 1, 1, 10, 100.00, 1000.00),
            (20010101, 2, 2, 20, 200.00, 2000.00),
            (20020101, 3, 3, 30, 300.00, 3000.00),
            (20030101, 4, 4, 40, 400.00, 4000.00),
            (20040101, 5, 5, 50, 500.00, 5000.00),
            (20050101, 6, 6, 60, 600.00, 6000.00)
    ) AS Sales (date, product, store, quantity, price, amount)
)
SELECT
    CASE
        WHEN SUM(CASE WHEN price > 100 THEN 1 ELSE 0 END) > 1 THEN 'Most orders are expensive'
        ELSE 'Most orders are cheap'
    END AS result
FROM Sales;