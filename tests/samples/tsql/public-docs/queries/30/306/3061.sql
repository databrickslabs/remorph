-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16

UPDATE dbo.Cities  
SET Location.X = 23.5  
WHERE Name = 'Anchorage';