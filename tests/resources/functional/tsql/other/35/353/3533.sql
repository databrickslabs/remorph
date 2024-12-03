--Query type: DCL
WITH RestoredDatabase AS (
    SELECT 'Sales2022' AS name, 'online' AS state_desc
)
SELECT *
FROM RestoredDatabase;
