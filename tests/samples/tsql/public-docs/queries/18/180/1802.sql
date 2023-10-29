-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-array-transact-sql?view=sql-server-ver16

DECLARE @id_value nvarchar(64) = NEWID();
SELECT JSON_ARRAY(1, @id_value, (SELECT @@SPID));