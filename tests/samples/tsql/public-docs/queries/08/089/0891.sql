-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

CREATE CLUSTERED INDEX [IDX_CL_MyFactTable]
ON dbo.[MyFactTable] ( ProductKey )
WITH ( DROP_EXISTING = ON );