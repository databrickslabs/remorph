-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-server-configuration-transact-sql?view=sql-server-ver16

ALTER SERVER CONFIGURATION   
SET PROCESS AFFINITY NUMANODE=0, 7;