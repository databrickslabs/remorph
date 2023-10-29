-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkfile-transact-sql?view=sql-server-ver16

USE UserDB;
GO
DBCC SHRINKFILE (DataFile1, 7);
GO