-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

ALTER INDEX mycolumnstoreindex ON dbo.mytable DISABLE;
-- update the data in mytable as necessary
ALTER INDEX mycolumnstoreindex on dbo.mytable REBUILD;