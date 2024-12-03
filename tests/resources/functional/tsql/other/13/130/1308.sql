--Query type: DDL
CREATE TABLE dbo.orders
(
    orderkey INT,
    totalprice DECIMAL(12, 2),
    discount DECIMAL(12, 2),
    discount_amount AS (totalprice * discount)
);

INSERT INTO dbo.orders (orderkey, totalprice, discount)
VALUES (1, 100.00, 0.10);

SELECT *
FROM dbo.orders;
-- REMORPH CLEANUP: DROP TABLE dbo.orders;
