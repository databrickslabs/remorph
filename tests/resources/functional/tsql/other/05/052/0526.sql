--Query type: DDL
SELECT 'ALTER DATABASE MyNewDatabase SET READ_COMMITTED_SNAPSHOT ON;' AS sql_statement
FROM (
    VALUES ('MyNewDatabase')
) AS temp_table(database_name);