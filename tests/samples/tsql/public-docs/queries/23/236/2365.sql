-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql?view=sql-server-ver16

SELECT * FROM sys.event_notifications  
WHERE name = 'Notify_ALTER_T1';