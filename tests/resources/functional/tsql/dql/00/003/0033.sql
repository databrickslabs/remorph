--Query type: DQL
WITH geography AS (
    SELECT 1 AS column1, 'City1' AS column2
    UNION ALL
    SELECT 2, 'City2'
    UNION ALL
    SELECT 3, 'City3'
)
-- Querying the simulated data
SELECT * FROM geography;
-- REMORPH CLEANUP: None needed for this query as it uses a CTE.