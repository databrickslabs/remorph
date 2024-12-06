-- tsql sql:
DECLARE @conversation_handle UNIQUEIDENTIFIER, @conversation_group_id UNIQUEIDENTIFIER;

SET @conversation_handle = '00000000-0000-0000-0000-000000000001';
SET @conversation_group_id = '00000000-0000-0000-0000-000000000002';

WITH MovedConversation AS (
    SELECT @conversation_handle AS conversation_handle, @conversation_group_id AS conversation_group_id
)

SELECT * FROM MovedConversation;
