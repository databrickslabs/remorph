--Query type: DCL
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'Buyers')
CREATE ROLE Buyers;

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'Sarah')
CREATE USER Sarah;

ALTER ROLE Buyers
ADD MEMBER Sarah;

SELECT *
FROM sys.database_role_members AS rm
INNER JOIN sys.database_principals AS r ON rm.role_principal_id = r.principal_id
INNER JOIN sys.database_principals AS m ON rm.member_principal_id = m.principal_id
WHERE r.name = 'Buyers';