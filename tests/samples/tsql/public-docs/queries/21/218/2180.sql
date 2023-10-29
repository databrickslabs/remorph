-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-trigger-transact-sql?view=sql-server-ver16

IF OBJECT_ID ('employee_insupd', 'TR') IS NOT NULL  
   DROP TRIGGER employee_insupd;