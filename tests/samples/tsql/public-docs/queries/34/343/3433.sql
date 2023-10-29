-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-symmetric-key-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GRANT ALTER ON SYMMETRIC KEY::SamInventory42 TO HamidS;  
GO