-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/indexkey-property-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT   
    INDEXKEY_PROPERTY(OBJECT_ID('Production.Location', 'U'),  
        1,1,'ColumnId') AS [Column ID],  
    INDEXKEY_PROPERTY(OBJECT_ID('Production.Location', 'U'),  
        1,1,'IsDescending') AS [Asc or Desc order];