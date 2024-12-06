-- tsql sql:
WITH EventNotifications AS (
    SELECT 'Notify_ALTER_T2' AS NotificationName, 'DATABASE' AS EventType, 'ALTER_TABLE' AS Event, 'NewNotifyService' AS ServiceName, '12345678-1234-1234-1234-123456789012' AS ServiceID
)
SELECT *
FROM EventNotifications;

SELECT *
FROM (
    VALUES ('Notify_ALTER_T2', 'DATABASE', 'ALTER_TABLE', 'NewNotifyService', '12345678-1234-1234-1234-123456789012')
) AS EventNotifications (NotificationName, EventType, Event, ServiceName, ServiceID);
