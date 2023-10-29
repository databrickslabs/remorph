-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/close-master-key-transact-sql?view=sql-server-ver16

USE master;  
OPEN MASTER KEY DECRYPTION BY PASSWORD = '43987hkhj4325tsku7';  
GO   
CLOSE MASTER KEY;  
GO