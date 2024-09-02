--Query type: DDL
DECLARE @sql NVARCHAR(MAX) = '';

WITH columns AS (
    SELECT 'column1' AS column_name, 'table1' AS table_name
    UNION ALL
    SELECT 'column2', 'table2'
)

SELECT @sql += 'DROP SENSITIVITY CLASSIFICATION FOR COLUMN ' + column_name + ' OF ' + table_name + '; '
FROM columns;

EXEC sp_executesql @sql;

SELECT * FROM table1;
SELECT * FROM table2;