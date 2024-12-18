-- tsql sql:
CREATE TABLE #temp_result
(
    OrderID INT,
    CustomerID INT,
    OrderDate DATE
);

INSERT INTO #temp_result
EXECUTE dbo.uspGetCustomerOrders;

INSERT INTO dbo.CustomerOrders
SELECT *
FROM #temp_result;

SELECT *
FROM dbo.CustomerOrders;

DROP TABLE #temp_result;
