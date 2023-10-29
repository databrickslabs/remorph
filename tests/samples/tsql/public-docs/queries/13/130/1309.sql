-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/table-value-constructor-transact-sql?view=sql-server-ver16

CREATE TABLE dbo.t (a INT, b CHAR);  
GO  
INSERT INTO dbo.t VALUES (1,'a'), (2, 1);  
GO