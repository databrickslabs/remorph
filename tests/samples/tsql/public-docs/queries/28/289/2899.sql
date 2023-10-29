-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-event-session-transact-sql?view=sql-server-ver16

SELECT name
    FROM sys.all_objects
    WHERE
        (name LIKE 'database[_]%' OR
         name LIKE 'server[_]%' )
        AND name LIKE '%[_]event%'
        AND type = 'V'
        AND SCHEMA_NAME(schema_id) = 'sys'
    ORDER BY name;