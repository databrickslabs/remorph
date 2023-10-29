-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkfile-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
-- Truncate the log by changing the database recovery model to SIMPLE.
ALTER DATABASE AdventureWorks2022
SET RECOVERY SIMPLE;
GO
-- Shrink the truncated log file to 1 MB.
DBCC SHRINKFILE (AdventureWorks2022_Log, 1);
GO
-- Reset the database recovery model.
ALTER DATABASE AdventureWorks2022
SET RECOVERY FULL;
GO