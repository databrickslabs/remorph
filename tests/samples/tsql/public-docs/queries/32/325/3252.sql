-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-encryption-key-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE DATABASE ENCRYPTION KEY  
WITH ALGORITHM = AES_256  
ENCRYPTION BY SERVER CERTIFICATE MyServerCert;  
GO