-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver16

SELECT CONCAT_WS(' - ', database_id, recovery_model_desc, containment_desc) AS DatabaseInfo
FROM sys.databases;