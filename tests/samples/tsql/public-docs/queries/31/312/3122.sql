-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkconstraints-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
CREATE TABLE Table1 (Col1 INT, Col2 CHAR(30));
GO
INSERT INTO Table1 VALUES (100, 'Hello');
GO
ALTER TABLE Table1 WITH NOCHECK ADD CONSTRAINT chkTab1 CHECK (Col1 > 100);
GO
DBCC CHECKCONSTRAINTS (Table1);
GO