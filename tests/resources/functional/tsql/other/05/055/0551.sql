--Query type: DDL
CREATE DATABASE database_name;
ALTER DATABASE database_name SET AUTO_UPDATE_STATISTICS_ASYNC OFF;
SELECT is_auto_update_stats_async_on FROM sys.databases WHERE name = 'database_name';
-- REMORPH CLEANUP: DROP DATABASE database_name;
