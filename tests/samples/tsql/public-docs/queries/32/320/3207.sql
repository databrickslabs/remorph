-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/deny-symmetric-key-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
DENY ALTER ON SYMMETRIC KEY::SamInventory42 TO HamidS;  
GO