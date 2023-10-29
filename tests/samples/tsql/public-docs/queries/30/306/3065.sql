-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/envelopeaggregate-geography-data-type?view=sql-server-ver16

USE AdventureWorks2022  
GO  
SELECT City,  
geography::EnvelopeAggregate(SpatialLocation) AS SpatialLocation  
FROM Person.Address  
WHERE PostalCode LIKE('981%')  
GROUP BY City;