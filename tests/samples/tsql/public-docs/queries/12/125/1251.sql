-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

CREATE TABLE [dbo].[data_retention_table]
(
  [dbdatetime2] datetime2(7),
  [product_code] int,
  [value] char(10)
)
WITH (DATA_DELETION = ON ( FILTER_COLUMN = [dbdatetime2], RETENTION_PERIOD = 1 WEEKS ))