-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/stats-date-transact-sql?view=sql-server-ver16

--Return the dates all statistics on the table were last updated.  
SELECT stats_id, name AS stats_name,   
    STATS_DATE(object_id, stats_id) AS statistics_date  
FROM sys.stats s  
WHERE s.object_id = OBJECT_ID('dbo.DimCustomer');  
GO