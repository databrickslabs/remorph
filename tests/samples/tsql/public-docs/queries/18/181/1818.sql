-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-path-exists-transact-sql?view=sql-server-ver16

DECLARE @jsonInfo NVARCHAR(MAX)

SET @jsonInfo=N'{"info":{"address":[{"town":"Paris"},{"town":"London"}]}}';

SELECT JSON_PATH_EXISTS(@jsonInfo,'$.info.address'); -- 1