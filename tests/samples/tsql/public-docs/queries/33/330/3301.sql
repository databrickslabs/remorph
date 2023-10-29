-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-default-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
IF EXISTS (SELECT name FROM sys.objects  
         WHERE name = 'datedflt'   
            AND type = 'D')  
   DROP DEFAULT datedflt;  
GO