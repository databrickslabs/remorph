-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/assemblyproperty-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT ASSEMBLYPROPERTY ('HelloWorld' , 'PublicKey');