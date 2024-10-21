--Query type: DDL
DECLARE @db_name sysname = 'current';
ALTER DATABASE [@db_name] MODIFY (EDITION = 'Premium');
SELECT * FROM sys.databases WHERE name = @db_name;
-- REMORPH CLEANUP: DROP TABLE IF EXISTS #db_name;