-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-encryption-key-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
ALTER DATABASE ENCRYPTION KEY  
REGENERATE WITH ALGORITHM = AES_256;  
GO