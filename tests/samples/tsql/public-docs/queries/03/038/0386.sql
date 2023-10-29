-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-table-as-select-transact-sql?view=sql-server-ver16

--CETAS write to a folder hierarchy (partitioned table):
CREATE EXTERNAL TABLE SalesOrdersExternalPartitioned
WITH (
    LOCATION = 'PartitionedOrders/year=*/month=*/', 
    DATA_SOURCE = CETASExternalDataSource,
    FILE_FORMAT = CETASFileFormat,
    --year and month will correspond to the two respective wildcards in folder path    
    PARTITION (
        [Year],
        [Month]
        ) 
    )
AS
    SELECT
        *,
        YEAR(OrderDate) AS [Year],
        MONTH(OrderDate) AS [Month]
    FROM [AdventureWorks2022].[Sales].[SalesOrderHeader]
    WHERE
        OrderDate < '2013-12-31';
GO

-- you can query the newly created partitioned external table
SELECT COUNT (*) FROM SalesOrdersExternalPartitioned;