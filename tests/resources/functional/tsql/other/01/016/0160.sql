--Query type: DDL
DECLARE @table_name sysname, @old_name sysname, @new_name sysname;
SELECT @table_name = table_name, @old_name = old_name, @new_name = new_name
FROM (
    VALUES ('customer', 'old_name', 'new_name')
) AS temp_table (table_name, old_name, new_name);
EXEC ('ALTER TABLE ' + @table_name + ' RENAME CONSTRAINT ' + @old_name + ' TO ' + @new_name);