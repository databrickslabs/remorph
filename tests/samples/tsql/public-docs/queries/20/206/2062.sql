-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/reconfigure-transact-sql?view=sql-server-ver16

EXEC sp_configure 'recovery interval', 75    
RECONFIGURE WITH OVERRIDE;    
GO