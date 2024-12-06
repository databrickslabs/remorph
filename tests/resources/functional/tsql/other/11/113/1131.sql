-- tsql sql:
SELECT 'CREATE SCHEMA Marketing' AS schema_creation_command
FROM (
    VALUES ('value1'),
           ('value2')
) AS temp_table(value);
