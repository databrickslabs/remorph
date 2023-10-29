-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

CREATE TABLE dbo.FactInternetSales2 (
    ProductKey [int] NOT NULL,
    OrderDateKey [int] NOT NULL,
    DueDateKey [int] NOT NULL,
    ShipDateKey [int] NOT NULL);

CREATE CLUSTERED COLUMNSTORE INDEX cci_FactInternetSales2
ON dbo.FactInternetSales2;

INSERT INTO dbo.FactInternetSales2
SELECT ProductKey, OrderDateKey, DueDateKey, ShipDateKey
FROM dbo.FactInternetSales;

SELECT * FROM sys.column_store_row_groups;