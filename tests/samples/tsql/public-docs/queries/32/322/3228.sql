-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-default-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
   BEGIN   
      EXEC sp_unbindefault 'Person.Contact.Phone'  
      DROP DEFAULT phonedflt  
   END;  
GO