--Query type: DML
DECLARE @myTable TABLE (column1 INT, column2 VARCHAR(10));
INSERT INTO @myTable (column1, column2)
VALUES (1, 'INITIAL'), (2, 'INITIAL');
UPDATE @myTable
SET column2 = 'TEST';
SELECT *
FROM @myTable;
-- REMORPH CLEANUP: DROP TABLE @myTable;