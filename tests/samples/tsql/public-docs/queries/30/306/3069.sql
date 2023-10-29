-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/convexhullaggregate-geography-data-type?view=sql-server-ver16

USE AdventureWorks2022  
GO  
SELECT geography::ConvexHullAggregate(SpatialLocation).ToString() AS SpatialLocation  
FROM Person.Address  
WHERE City LIKE ('Bothell')