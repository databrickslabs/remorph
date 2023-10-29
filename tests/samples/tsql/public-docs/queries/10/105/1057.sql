-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

CREATE NONCLUSTERED COLUMNSTORE INDEX csindx_simple
ON SimpleTable (OrderDateKey, DueDateKey, ShipDateKey)
WITH (DROP_EXISTING =  ON,
    MAXDOP = 2)
ON "DEFAULT";
GO