-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-server-configuration-transact-sql?view=sql-server-ver16

ALTER SERVER CONFIGURATION   
SET BUFFER POOL EXTENSION ON  
    (FILENAME = 'F:\SSDCACHE\Example.BPE', SIZE = 50 GB);