-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE tempdb;
GO

CREATE TABLE dbo.table1
(
    id INT,
    employee VARCHAR(32)
);
GO
  
INSERT INTO dbo.table1
VALUES (1, 'Fred'),
    (2, 'Tom'),
    (3, 'Sally'),
    (4, 'Alice');
GO
  
DECLARE @MyTableVar TABLE (
    id INT,
    employee VARCHAR(32)
);

PRINT 'table1, before delete';

SELECT *
FROM dbo.table1;

DELETE
FROM dbo.table1
OUTPUT DELETED.*
INTO @MyTableVar
WHERE id = 4
    OR id = 2;

PRINT 'table1, after delete';

SELECT *
FROM dbo.table1;

PRINT '@MyTableVar, after delete';

SELECT *
FROM @MyTableVar;

DROP TABLE dbo.table1;