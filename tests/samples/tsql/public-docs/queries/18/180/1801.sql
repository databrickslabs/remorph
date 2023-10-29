-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-object-transact-sql?view=sql-server-ver16

DECLARE @id_key nvarchar(10) = N'id',@id_value nvarchar(64) = NEWID();
SELECT JSON_OBJECT('user_name':USER_NAME(), @id_key:@id_value, 'sid':(SELECT @@SPID))