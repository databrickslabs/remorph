-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/partition-transact-sql?view=sql-server-ver16

CREATE PARTITION SCHEME RangePS1  
    AS PARTITION RangePF1  
    ALL TO ('PRIMARY') ;  
GO  

CREATE TABLE dbo.PartitionTable (col1 int PRIMARY KEY, col2 char(10))  
    ON RangePS1 (col1) ;  
GO

INSERT dbo.PartitionTable (col1, col2)
VALUES ((1,'a row'),(100,'another row'),(500,'another row'),(1000,'another row'))


SELECT 
	$PARTITION.RangePF1(col1) AS Partition,   
	COUNT(*) AS [COUNT] 
FROM dbo.PartitionTable
GROUP BY $PARTITION.RangePF1(col1)  
ORDER BY Partition ;  
GO