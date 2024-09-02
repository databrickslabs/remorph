--Query type: DQL
WITH EmployeeCTE AS (
    SELECT CAST(n_nationkey AS VARCHAR(10)) AS NationKey,
           CAST(n_name AS VARCHAR(50)) AS NationName
    FROM (
        VALUES (1, 'Nation1'),
               (2, 'Nation2'),
               (3, 'Nation3')
    ) AS NationTable (n_nationkey, n_name)
)
SELECT NationKey,
       NationName.ToString() AS NationNode
FROM EmployeeCTE
ORDER BY NationKey;