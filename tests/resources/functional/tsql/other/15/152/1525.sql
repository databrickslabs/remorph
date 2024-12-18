-- tsql sql:
DECLARE @conversation_handle UNIQUEIDENTIFIER;
SET @conversation_handle = 'conversation_handle_1';

WITH ExpenseQueueCTE AS (
    SELECT conversation_handle, message_body
    FROM (
        VALUES ('conversation_handle_1', 'message_body_1'),
               ('conversation_handle_2', 'message_body_2'),
               ('conversation_handle_3', 'message_body_3')
    ) AS ExpenseQueue(conversation_handle, message_body)
)

SELECT *
FROM ExpenseQueueCTE
WHERE conversation_handle = @conversation_handle;
