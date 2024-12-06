-- tsql sql:
DECLARE @dialog_handle UNIQUEIDENTIFIER = NEWID();
SELECT @dialog_handle AS DialogHandle
FROM (VALUES (1)) AS temp_result(any_column);
