-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/revoke-transact-sql?view=sql-server-ver16

CREATE SCHEMA Sales;  
GO
CREATE USER Joe without login;
GO
CREATE ROLE Vendors;
GO
ALTER ROLE Vendors ADD MEMBER Joe; 
GO
GRANT SELECT ON SCHEMA :: Sales TO Vendors;
GO
REVOKE SELECT ON SCHEMA :: Sales TO Vendors;
GO