-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-recommendations-sql?view=azure-sqldw-latest

-- Step 2: view advice generated for the above workload
DECLARE @sessionid nvarchar(100), @recommendation nvarchar(max);
SELECT @sessionid = SESSION_ID();
SELECT @recommendation = recommendation FROM sys.dm_pdw_distrib_advisor_results WHERE session_id = @sessionid;
SELECT @recommendation;
GO