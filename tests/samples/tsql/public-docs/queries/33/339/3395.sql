-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/stats-date-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT name AS stats_name,   
    STATS_DATE(object_id, stats_id) AS statistics_update_date  
FROM sys.stats   
WHERE object_id = OBJECT_ID('Person.Address');  
GO