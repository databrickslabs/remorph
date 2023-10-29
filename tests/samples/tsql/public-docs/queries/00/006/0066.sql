-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-opentran-transact-sql?view=sql-server-ver16

-- Create the temporary table to accept the results.
CREATE TABLE #OpenTranStatus (
   ActiveTransaction VARCHAR(25),
   Details sql_variant
   );
-- Execute the command, putting the results in the table.
INSERT INTO #OpenTranStatus
   EXEC ('DBCC OPENTRAN WITH TABLERESULTS, NO_INFOMSGS');
  
-- Display the results.
SELECT * FROM #OpenTranStatus;
GO