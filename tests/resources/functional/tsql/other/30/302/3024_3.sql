-- tsql sql:
CREATE TABLE temp_result (order_key INT IDENTITY(1,1) NOT NULL, totalprice DECIMAL(10, 2) NOT NULL);
WITH temp_result AS (
    SELECT order_key, totalprice
    FROM (
        VALUES (1, 100.00), (2, 200.00)
    ) AS temp_result(order_key, totalprice)
)
SELECT * FROM temp_result
