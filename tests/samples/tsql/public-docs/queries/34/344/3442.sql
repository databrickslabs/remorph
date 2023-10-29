-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-symmetric-key-permissions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
REVOKE ALTER ON SYMMETRIC KEY::SamInventory42 TO HamidS CASCADE;  
GO