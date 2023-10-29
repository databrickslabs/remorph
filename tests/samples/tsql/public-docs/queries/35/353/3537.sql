-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-server-role-transact-sql?view=sql-server-ver16

USE master;  
CREATE SERVER ROLE buyers AUTHORIZATION BenMiller;  
GO