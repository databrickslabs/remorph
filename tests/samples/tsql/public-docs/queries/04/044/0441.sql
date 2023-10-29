-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

--Prepare the example by creating a table with a clustered columnstore index.
CREATE TABLE SimpleTable (
    ProductKey [int] NOT NULL,
    OrderDateKey [int] NOT NULL,
    DueDateKey [int] NOT NULL,
    ShipDateKey [int] NOT NULL
);

CREATE CLUSTERED INDEX cci_SimpleTable ON SimpleTable (ProductKey);

CREATE CLUSTERED COLUMNSTORE INDEX cci_SimpleTable
ON SimpleTable
WITH (DROP_EXISTING = ON);

--Compress the table further by using archival compression.
ALTER INDEX cci_SimpleTable ON SimpleTable
REBUILD
WITH (DATA_COMPRESSION = COLUMNSTORE_ARCHIVE);
GO