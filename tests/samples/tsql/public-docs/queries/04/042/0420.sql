-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

--Create the table for use with this example.
CREATE TABLE dbo.SimpleTable (
    ProductKey [INT] NOT NULL,
    OrderDateKey [INT] NOT NULL,
    DueDateKey [INT] NOT NULL,
    ShipDateKey [INT] NOT NULL);
GO
  
--Create two nonclustered indexes for use with this example
CREATE INDEX nc1_simple ON dbo.SimpleTable (OrderDateKey);
CREATE INDEX nc2_simple ON dbo.SimpleTable (DueDateKey);
GO