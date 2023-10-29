-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver16

SELECT STRING_AGG(CONCAT_WS(',', database_id, recovery_model_desc, containment_desc), CHAR(13)) AS DatabaseInfo
FROM sys.databases;