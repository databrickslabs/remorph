-- tsql sql:
SELECT DATABASEPROPERTYEX('AdventureWorks2022', 'Collation') AS Collation,
       DATABASEPROPERTYEX('AdventureWorks2022', 'Edition') AS Edition,
       DATABASEPROPERTYEX('AdventureWorks2022', 'ServiceObjective') AS ServiceObjective,
       DATABASEPROPERTYEX('AdventureWorks2022', 'MaxSizeInBytes') AS MaxSizeInBytes
FROM (
    VALUES (1)
) AS temp(dummy);
