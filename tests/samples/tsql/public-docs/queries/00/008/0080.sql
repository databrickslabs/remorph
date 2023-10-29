-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

-- Example is based on AdventureWorks
CREATE EXTERNAL TABLE dbo.FactInternetSalesNew
    WITH (
            LOCATION = '/files/Customer',
            DATA_SOURCE = customer_ds,
            FILE_FORMAT = customer_ff
            ) AS

SELECT T1.*
FROM dbo.FactInternetSales T1
INNER JOIN dbo.DimCustomer T2
    ON (T1.CustomerKey = T2.CustomerKey)
OPTION (HASH JOIN);
GO