--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'Customer#000000001' AS name,
           'United States' AS nation
),
     NationCTE AS (
    SELECT 'United States' AS name,
           'North America' AS region
)
SELECT C.name AS CustomerName,
       N.name AS NationName
FROM CustomerCTE AS C
     INNER JOIN NationCTE AS N
     ON C.nation = N.name
ORDER BY C.name;