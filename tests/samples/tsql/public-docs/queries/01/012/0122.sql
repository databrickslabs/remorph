-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-ansi-defaults-transact-sql?view=sql-server-ver16

-- SET ANSI_DEFAULTS ON.  
SET ANSI_DEFAULTS ON;  
GO  

-- Display the current settings.  
DBCC USEROPTIONS;  
GO 

-- SET ANSI_DEFAULTS OFF.  
SET ANSI_DEFAULTS OFF;  
GO