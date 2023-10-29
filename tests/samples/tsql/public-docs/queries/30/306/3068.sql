-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/collectionaggregate-geography-data-type?view=sql-server-ver16

USE AdventureWorks2022  
GO  
SELECT geography::CollectionAggregate(SpatialLocation).ToString() AS SpatialLocation  
FROM Person.Address  
WHERE City LIKE ('Bothell')