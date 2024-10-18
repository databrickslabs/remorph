--Query type: DDL
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'my_database')
BEGIN
    CREATE DATABASE [my_database];
END
ALTER DATABASE [my_database] SET AUTO_CLOSE OFF;
WITH database_properties AS (
    SELECT name, is_auto_close_on FROM sys.databases WHERE name = 'my_database'
)
SELECT * FROM database_properties;
-- REMORPH CLEANUP: DROP DATABASE [my_database];