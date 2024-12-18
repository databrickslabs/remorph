-- tsql sql:
SELECT Edition = DATABASEPROPERTYEX(database_name, 'EDITION'),
       ServiceObjective = DATABASEPROPERTYEX(database_name, 'ServiceObjective'),
       MaxSizeInBytes = DATABASEPROPERTYEX(database_name, 'MaxSizeInBytes')
FROM (
    VALUES ('db1')
) AS db_properties (
    database_name
);
