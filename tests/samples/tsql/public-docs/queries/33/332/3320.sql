-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/index-col-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT   
    INDEX_COL (N'AdventureWorks2022.Sales.SalesOrderDetail', 1,1) AS  
        [Index Column 1],   
    INDEX_COL (N'AdventureWorks2022.Sales.SalesOrderDetail', 1,2) AS  
        [Index Column 2]  
;  
GO