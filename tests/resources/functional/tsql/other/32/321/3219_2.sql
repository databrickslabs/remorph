-- tsql sql:
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
SELECT *
FROM (
    VALUES (1, 'a'),
           (2, 'b')
) AS temp_table (column1, column2);
