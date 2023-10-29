-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-ver16

UPDATE Cities  
SET Location.SetXY(23.5, 23.5)  
WHERE Name = 'Anchorage';