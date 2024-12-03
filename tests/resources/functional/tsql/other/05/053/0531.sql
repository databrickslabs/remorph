--Query type: DDL
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
ALTER DATABASE SCOPED CONFIGURATION CLEAR PROCEDURE_CACHE;
SELECT *
FROM (
    VALUES (
        1, 'config_option', 'value'
    )
) AS temp_result(id, name, value)
WHERE name = 'MAXDOP';
