--Query type: DDL
CREATE TABLE dbo.orders_example (
    o_orderkey INT NOT NULL,
    o_custkey INT NOT NULL,
    o_totalprice DECIMAL(10, 2) NOT NULL,
    CONSTRAINT total_price_cap CHECK (o_totalprice < 100000)
);
-- REMORPH CLEANUP: DROP TABLE dbo.orders_example;