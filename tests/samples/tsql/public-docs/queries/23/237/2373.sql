-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql?view=sql-server-ver16

SELECT * FROM sys.server_event_notifications  
WHERE name = 'log_ddl1';