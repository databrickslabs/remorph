--Query type: DDL
CREATE TABLE orders (
    order_key INT PRIMARY KEY NOT NULL,
    totalprice DECIMAL(10, 2) NOT NULL,
    orderdate DATE NOT NULL
);

WITH temp_result AS (
    SELECT *
    FROM (
        VALUES (1, 100.00, '2020-01-01'),
               (2, 200.00, '2020-01-02')
    ) AS temp_table (order_key, totalprice, orderdate)
)
INSERT INTO orders (order_key, totalprice, orderdate)
SELECT *
FROM temp_result;

SELECT *
FROM orders;
-- REMORPH CLEANUP: DROP TABLE orders;