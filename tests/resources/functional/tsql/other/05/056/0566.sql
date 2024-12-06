-- tsql sql:
DECLARE @query nvarchar(max);

WITH newdb AS (
    SELECT 'newdb' AS name
),
newserver AS (
    SELECT 'newserver' AS name
)

SELECT @query = 'ALTER DATABASE ' + newdb.name + ' REMOVE SECONDARY ON SERVER ' + newserver.name
FROM newdb, newserver;

EXECUTE sp_executesql @query;

-- REMORPH CLEANUP: DROP DATABASE newdb;
-- REMORPH CLEANUP: DROP SERVER newserver;
