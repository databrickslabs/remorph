-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkfile-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
-- Create a data file and assume it contains data.
ALTER DATABASE AdventureWorks2022
ADD FILE (
    NAME = Test1data,
    FILENAME = 'C:\t1data.ndf',
    SIZE = 5MB
    );
GO
-- Empty the data file.
DBCC SHRINKFILE (Test1data, EMPTYFILE);
GO
-- Remove the data file from the database.
ALTER DATABASE AdventureWorks2022
REMOVE FILE Test1data;
GO