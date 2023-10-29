-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/table-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
IF OBJECT_ID (N'Sales.ufn_SalesByStore', N'IF') IS NOT NULL
    DROP FUNCTION Sales.ufn_SalesByStore;
GO
CREATE FUNCTION Sales.ufn_SalesByStore (@storeid int)
RETURNS TABLE
AS
RETURN
(
    SELECT P.ProductID,
        P.Name,
        SUM(SD.LineTotal) AS 'Total'
    FROM Production.Product AS P
    INNER JOIN Sales.SalesOrderDetail AS SD
        ON SD.ProductID = P.ProductID
    INNER JOIN Sales.SalesOrderHeader AS SH
        ON SH.SalesOrderID = SD.SalesOrderID
    INNER JOIN Sales.Customer AS C
        ON SH.CustomerID = C.CustomerID
    WHERE C.StoreID = @storeid
    GROUP BY P.ProductID,
        P.Name
);
GO