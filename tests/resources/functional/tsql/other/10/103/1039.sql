-- tsql sql:
CREATE LOGIN [AdventureWorks\John] WITH PASSWORD = 'password';

WITH ConfigSettings AS (
    SELECT name, value, value_in_use
    FROM sys.configurations
    WHERE name LIKE '%remote%'
)
SELECT * FROM ConfigSettings;

SELECT * FROM sys.server_principals WHERE name = 'AdventureWorks\John';

-- REMORPH CLEANUP: DROP LOGIN [AdventureWorks\John];
