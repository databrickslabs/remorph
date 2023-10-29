-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

CREATE TABLE dbo.SimpleTable2 (
    ProductKey [INT] NOT NULL,
    OrderDateKey [INT] NOT NULL,
    DueDateKey [INT] NOT NULL,
    ShipDateKey [INT] NOT NULL);
GO
CREATE CLUSTERED INDEX cl_simple ON dbo.SimpleTable2 (ProductKey);
GO
CREATE CLUSTERED COLUMNSTORE INDEX cl_simple ON dbo.SimpleTable2
WITH (DROP_EXISTING = ON);
GO