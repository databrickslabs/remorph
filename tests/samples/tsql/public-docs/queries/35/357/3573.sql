-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-server-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE GRANT OPTION FOR CONNECT SQL FROM JanethEsteves;  
GO