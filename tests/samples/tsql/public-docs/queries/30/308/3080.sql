-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @CustomerTimeZone nvarchar(128) = 'Central European Standard Time';

SELECT SalesOrderID, OrderDate,
    --Assign the known offset only
    OrderDate AT TIME ZONE 'Pacific Standard Time' AS OrderDate_TimeZonePST,
    --Assign the known offset, then convert to another time zone
    OrderDate AT TIME ZONE 'Pacific Standard Time' AT TIME ZONE @CustomerTimeZone AS OrderDate_TimeZoneCustomer
FROM Sales.SalesOrderHeader;