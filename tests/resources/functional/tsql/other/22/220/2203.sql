--Query type: DML
CREATE TABLE SalesSummary
(
    CustomerID INT,
    CustomerName VARCHAR(255),
    OrderTotal DECIMAL(10, 2),
    OrderDate DATE
);

WITH SalesData AS
(
    SELECT TOP (5) c.c_custkey, c.c_name, c.o_totalprice, o.o_orderdate
    FROM (
        VALUES (1, 'Customer1', 100.00, '2020-01-01'),
               (2, 'Customer2', 200.00, '2020-01-15'),
               (3, 'Customer3', 300.00, '2020-02-01'),
               (4, 'Customer4', 400.00, '2020-03-01'),
               (5, 'Customer5', 500.00, '2020-04-01')
    ) AS c (c_custkey, c_name, o_totalprice, o_orderdate)
    INNER JOIN (
        VALUES (1, '2020-01-01'),
               (2, '2020-01-15'),
               (3, '2020-02-01'),
               (4, '2020-03-01'),
               (5, '2020-04-01')
    ) AS o (o_orderkey, o_orderdate)
    ON c.c_custkey = o.o_orderkey
    WHERE c.o_totalprice > 250.00
)
INSERT INTO SalesSummary (CustomerID, CustomerName, OrderTotal, OrderDate)
SELECT c_custkey, c_name, o_totalprice, o_orderdate
FROM SalesData
ORDER BY o_totalprice DESC;

SELECT * FROM SalesSummary;
-- REMORPH CLEANUP: DROP TABLE SalesSummary;
