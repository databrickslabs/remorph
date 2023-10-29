-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql?view=sql-server-ver16

CREATE EVENT NOTIFICATION Notify_ALTER_T1  
ON DATABASE  
FOR ALTER_TABLE  
TO SERVICE 'NotifyService',  
    '8140a771-3c4b-4479-8ac0-81008ab17984';