-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-server-principal-permissions-transact-sql?view=sql-server-ver16

USE master;  
REVOKE IMPERSONATE ON LOGIN::WanidaBenshoof FROM [AdvWorks\YoonM];  
GO