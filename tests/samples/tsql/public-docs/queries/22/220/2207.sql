-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/table-value-constructor-transact-sql?view=sql-server-ver16

INSERT INTO dbo.t VALUES (1,'a'), (2, CONVERT(CHAR,1));