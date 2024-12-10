-- tsql sql:
CREATE USER John WITHOUT LOGIN;
GRANT EXECUTE ON pr_CustomerInfo TO John;
REVOKE EXECUTE ON pr_CustomerInfo FROM John;
SELECT * FROM sys.database_principals WHERE name = 'John';
-- REMORPH CLEANUP: DROP USER John;
