-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-sequence-transact-sql?view=sql-server-ver16

SELECT cache_size, current_value   
FROM sys.sequences  
WHERE name = 'DecSeq' ;