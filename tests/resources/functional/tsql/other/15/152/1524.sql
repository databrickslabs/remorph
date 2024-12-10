-- tsql sql:
DECLARE @conversation_group_id UNIQUEIDENTIFIER;

SELECT @conversation_group_id = conversation_group_id
FROM (
    VALUES
        (NEWID(), 'Message 1'),
        (NEWID(), 'Message 2'),
        (NEWID(), 'Message 3')
) AS MyQueue(conversation_group_id, message)
WHERE message = 'Message 1';

SELECT @conversation_group_id AS conversation_group_id;
