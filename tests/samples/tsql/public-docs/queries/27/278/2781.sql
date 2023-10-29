-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/symkeyproperty-transact-sql?view=sql-server-ver16

SELECT SYMKEYPROPERTY(256, 'algorithm_desc') AS Algorithm ;  
GO