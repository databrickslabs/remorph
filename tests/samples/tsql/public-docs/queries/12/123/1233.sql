-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-opentran-transact-sql?view=sql-server-ver16

CREATE TABLE T1(Col1 INT, Col2 CHAR(3));
GO
BEGIN TRAN
INSERT INTO T1 VALUES (101, 'abc');
GO
DBCC OPENTRAN;
ROLLBACK TRAN;
GO
DROP TABLE T1;
GO