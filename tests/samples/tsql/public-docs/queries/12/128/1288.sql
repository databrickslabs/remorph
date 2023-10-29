-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-inputbuffer-transact-sql?view=sql-server-ver16

CREATE TABLE dbo.T1 (Col1 INT, Col2 CHAR(3));
GO

DECLARE @i INT = 0;

BEGIN TRANSACTION

SET @i = 0;

WHILE (@i < 100000)
BEGIN
    INSERT INTO dbo.T1
    VALUES (@i, CAST(@i AS CHAR(3)));
    SET @i += 1;
END;

COMMIT TRANSACTION;

--Start new connection #2.
DBCC INPUTBUFFER (52);