-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-deadlock-priority-transact-sql?view=sql-server-ver16

DECLARE @deadlock_var NCHAR(3);
SET @deadlock_var = N'LOW';
  
SET DEADLOCK_PRIORITY @deadlock_var;
GO