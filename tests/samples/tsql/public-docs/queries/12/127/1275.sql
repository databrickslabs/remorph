-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

CREATE TABLE dbo.SimpleTable(
    ProductKey [INT] NOT NULL,
    OrderDateKey [INT] NOT NULL,
    DueDateKey [INT] NOT NULL,
    ShipDateKey [INT] NOT NULL);
GO
CREATE CLUSTERED COLUMNSTORE INDEX cci_Simple ON dbo.SimpleTable;
GO