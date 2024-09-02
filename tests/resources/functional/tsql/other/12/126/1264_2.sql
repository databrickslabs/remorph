--Query type: DML
CREATE TABLE #CustomerOrders
(
    CustomerID INT,
    OrderDate DATE,
    TotalSales DECIMAL(10, 2)
);

DECLARE @MyTableVar TABLE
(
    CustomerID INT,
    OrderDate DATE,
    TotalSales DECIMAL(10, 2)
);

WITH Customer AS
(
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer 1', 'Address 1'),
               (2, 'Customer 2', 'Address 2'),
               (3, 'Customer 3', 'Address 3')
    ) AS c (c_custkey, c_name, c_address)
),
Orders AS
(
    SELECT o_orderkey, o_orderdate, o_custkey
    FROM (
        VALUES (1, '2020-01-01', 1),
               (2, '2020-01-15', 2),
               (3, '2020-02-01', 3)
    ) AS o (o_orderkey, o_orderdate, o_custkey)
),
OrderLines AS
(
    SELECT ol_orderkey, ol_linenumber, ol_amount
    FROM (
        VALUES (1, 1, 100.00),
               (2, 2, 200.00),
               (3, 3, 300.00)
    ) AS ol (ol_orderkey, ol_linenumber, ol_amount)
)
INSERT INTO #CustomerOrders (CustomerID, OrderDate, TotalSales)
OUTPUT INSERTED.CustomerID, INSERTED.OrderDate, INSERTED.TotalSales
INTO @MyTableVar (CustomerID, OrderDate, TotalSales)
SELECT c.c_custkey, o.o_orderdate, SUM(ol.ol_amount) AS TotalSales
FROM Customer c
INNER JOIN Orders o ON c.c_custkey = o.o_custkey
INNER JOIN OrderLines ol ON o.o_orderkey = ol.ol_orderkey
WHERE o.o_orderkey LIKE '1%'
GROUP BY c.c_custkey, o.o_orderdate
ORDER BY c.c_custkey, o.o_orderdate;

SELECT * FROM #CustomerOrders;
SELECT * FROM @MyTableVar;
-- REMORPH CLEANUP: DROP TABLE #CustomerOrders;
-- REMORPH CLEANUP: DROP TABLE @MyTableVar;