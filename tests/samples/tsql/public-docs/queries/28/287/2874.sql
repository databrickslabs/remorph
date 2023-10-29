-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/partition-transact-sql?view=sql-server-ver16

SELECT col1, col2
FROM dbo.PartitionTable
WHERE $PARTITION.RangePF1(col1) = 3 ;