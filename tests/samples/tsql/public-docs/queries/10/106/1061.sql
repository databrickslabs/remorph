-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

CREATE NONCLUSTERED INDEX IX_INDEX_1
  ON T1 (C2)
  WITH (XML_COMPRESSION = ON);
GO