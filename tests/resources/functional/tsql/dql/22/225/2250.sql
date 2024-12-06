-- tsql sql:
WITH ExpenseCTE AS (
    SELECT CAST('conversation_handle' AS UNIQUEIDENTIFIER) AS conversation_handle,
           CAST('message_type_name' AS sysname) AS message_type_name,
           CAST('message_body' AS VARBINARY(MAX)) AS message_body
)
SELECT conversation_handle,
       message_type_name,
       message_body
FROM ExpenseCTE;
