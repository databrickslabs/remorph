-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-signature-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
DROP SIGNATURE FROM HumanResources.uspUpdateEmployeeLogin   
    BY CERTIFICATE HumanResourcesDP;  
GO