--Query type: DDL
DECLARE @sql_command nvarchar(max) = 'ALTER DATABASE [database_name] SET RECOVERY FULL PAGE_VERIFY CHECKSUM;';
SELECT @sql_command AS sql_command
FROM (
    VALUES ('dummy_value')
) AS temp_result(value);
EXEC sp_executesql @sql_command;
