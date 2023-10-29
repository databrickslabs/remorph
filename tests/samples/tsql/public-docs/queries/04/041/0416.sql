-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Create the clustered columnstore index,
--replacing the existing rowstore clustered index of the same name
CREATE CLUSTERED COLUMNSTORE
INDEX [IDX_CL_MyFactTable]
ON dbo.MyFactTable
WITH (DROP_EXISTING = ON);