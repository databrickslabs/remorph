-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
CREATE EXTERNAL TABLE SalesOrdersPerYear
WITH
(
    LOCATION = 'hdfs://xxx.xxx.xxx.xxx:5000/files/Customer',
    FORMAT_OPTIONS ( FIELD_TERMINATOR = '|' )
)
AS
    -- Define the CTE expression name and column list.
    WITH Sales_CTE (SalesPersonID, SalesOrderID, SalesYear)
    AS
    -- Define the CTE query.
    (
        SELECT SalesPersonID, SalesOrderID, YEAR(OrderDate) AS SalesYear
        FROM Sales.SalesOrderHeader
        WHERE SalesPersonID IS NOT NULL
    )
    -- Define the outer query referencing the CTE name.
    SELECT SalesPersonID, COUNT(SalesOrderID) AS TotalSales, SalesYear
    FROM Sales_CTE
    GROUP BY SalesYear, SalesPersonID
    ORDER BY SalesPersonID, SalesYear;
GO