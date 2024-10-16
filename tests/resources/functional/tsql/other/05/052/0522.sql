--Query type: DDL
CREATE DATABASE NewDB;
ALTER DATABASE NewDB MODIFY FILE (NAME = N'NewDB_log', SIZE = 5GB);
SELECT name, database_id, create_date FROM sys.databases WHERE name = 'NewDB';
-- REMORPH CLEANUP: DROP DATABASE NewDB;