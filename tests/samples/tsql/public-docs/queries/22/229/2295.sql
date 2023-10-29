-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/databasepropertyex-transact-sql?view=sql-server-ver16

SELECT   
    DATABASEPROPERTYEX('AdventureWorks2022', 'Collation') AS Collation,  
    DATABASEPROPERTYEX('AdventureWorks2022', 'Edition') AS Edition,  
    DATABASEPROPERTYEX('AdventureWorks2022', 'ServiceObjective') AS ServiceObjective,  
    DATABASEPROPERTYEX('AdventureWorks2022', 'MaxSizeInBytes') AS MaxSizeInBytes