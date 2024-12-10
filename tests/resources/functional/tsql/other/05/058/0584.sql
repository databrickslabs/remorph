-- tsql sql:
DECLARE @search_property_list_name nvarchar(100) = 'spl_2';
CREATE TABLE table_1
(
    id INT PRIMARY KEY,
    column_name nvarchar(100)
);
CREATE FULLTEXT INDEX ON table_1 (column_name) KEY INDEX PK_table_1;
DECLARE @sql nvarchar(max) = N'ALTER FULLTEXT INDEX ON table_1 SET SEARCH PROPERTY LIST ''' + @search_property_list_name + '''';
EXEC sp_executesql @sql;
SELECT * FROM table_1;
-- REMORPH CLEANUP: DROP TABLE table_1;
-- REMORPH CLEANUP: DROP FULLTEXT INDEX ON table_1;
