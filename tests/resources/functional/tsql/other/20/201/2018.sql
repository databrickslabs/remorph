--Query type: DDL
CREATE TABLE #orders
(
    order_id INT,
    total_cost DECIMAL(10, 2)
);

INSERT INTO #orders (order_id, total_cost)
VALUES
    (1, 10.99),
    (2, 5.99),
    (3, 7.99);

DROP SENSITIVITY CLASSIFICATION FROM #orders.total_cost;

SELECT *
FROM #orders;

-- REMORPH CLEANUP: DROP TABLE #orders;