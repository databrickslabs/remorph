-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-server-role-transact-sql?view=sql-server-ver16

SELECT SP1.name AS RoleOwner, SP2.name AS Server_Role  
FROM sys.server_principals AS SP1  
JOIN sys.server_principals AS SP2  
    ON SP1.principal_id = SP2.owning_principal_id   
ORDER BY SP1.name ;