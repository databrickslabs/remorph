--Query type: DDL
WITH SchemaInfo AS (SELECT 'SchemaY' AS SchemaName, 'User1' AS AuthorizationUser)
SELECT 'CREATE SCHEMA ' + SchemaName + ' AUTHORIZATION ' + AuthorizationUser AS SchemaCreationQuery
FROM SchemaInfo
