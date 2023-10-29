-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-default-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
sp_bindefault 'phonedflt', 'Person.PersonPhone.PhoneNumber';