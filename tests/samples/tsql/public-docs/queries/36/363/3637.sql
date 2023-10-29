-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16

WITH
CountDate (TotalCount, TableName) AS
    (
     SELECT COUNT(datekey), 'DimDate' FROM DimDate
    ) ,
CountCustomer (TotalAvg, TableName) AS
    (
     SELECT COUNT(CustomerKey), 'DimCustomer' FROM DimCustomer
    )
SELECT TableName, TotalCount FROM CountDate
UNION ALL
SELECT TableName, TotalAvg FROM CountCustomer;