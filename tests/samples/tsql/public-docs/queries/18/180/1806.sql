-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checktable-transact-sql?view=sql-server-ver16

DECLARE @indid int;
SET @indid = (SELECT index_id
              FROM sys.indexes
              WHERE object_id = OBJECT_ID('Production.Product')
                    AND name = 'AK_Product_Name');
DBCC CHECKTABLE ('Production.Product',@indid);