-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-event-notification-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE EVENT NOTIFICATION NotifyALTER_T1  
ON DATABASE  
FOR ALTER_TABLE  
TO SERVICE 'NotifyService',  
    '8140a771-3c4b-4479-8ac0-81008ab17984';  
GO  
DROP EVENT NOTIFICATION NotifyALTER_T1  
ON DATABASE;