-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-compatibility-level?view=sql-server-ver16

DROP TABLE IF EXISTS t1;
GO

CREATE TABLE t1 (c1 time(7), c2 datetime2);
GO

INSERT t1 (c1,c2) VALUES (GETDATE(), GETDATE());
GO

SELECT CONVERT(nvarchar(16),c1,0) AS TimeStyle0
       ,CONVERT(nvarchar(16),c1,121)AS TimeStyle121
       ,CONVERT(nvarchar(32),c2,0) AS Datetime2Style0
       ,CONVERT(nvarchar(32),c2,121)AS Datetime2Style121
FROM t1;
GO