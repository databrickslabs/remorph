-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/partition-transact-sql?view=sql-server-ver16

CREATE PARTITION FUNCTION RangePF1 ( INT )  
AS RANGE LEFT FOR VALUES (10, 100, 1000) ;  
GO

SELECT $PARTITION.RangePF1 (10) ;  
GO