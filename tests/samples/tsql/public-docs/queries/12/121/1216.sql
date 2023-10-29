-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

CREATE TABLE PartitionTable (col1 INT, col2 CHAR(10))
ON myRangePS1 (col1) ;
GO
CREATE TABLE NonPartitionTable (col1 INT, col2 CHAR(10))
ON test2fg ;
GO
ALTER TABLE PartitionTable SWITCH PARTITION 2 TO NonPartitionTable ;
GO