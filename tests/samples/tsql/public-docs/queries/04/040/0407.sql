-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Create a rowstore table with a clustered index and a nonclustered index.
CREATE TABLE dbo.MyFactTable (
    ProductKey [INT] NOT NULL,
    OrderDateKey [INT] NOT NULL,
    DueDateKey [INT] NOT NULL,
    ShipDateKey [INT] NOT NULL
INDEX IDX_CL_MyFactTable CLUSTERED  ( ProductKey )
);

--Add a nonclustered index.
CREATE INDEX my_index ON dbo.MyFactTable ( ProductKey, OrderDateKey );