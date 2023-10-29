-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-showcontig-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
DECLARE @id INT, @indid INT
SET @id = OBJECT_ID('Production.Product');

SELECT @indid = index_id
FROM sys.indexes
WHERE object_id = @id
   AND name = 'AK_Product_Name';

DBCC SHOWCONTIG (@id, @indid);
GO