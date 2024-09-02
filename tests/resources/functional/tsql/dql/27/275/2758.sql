--Query type: DQL
WITH CustomerCTE AS (
    SELECT customer_key, name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer(customer_key, name)
),
NationCTE AS (
    SELECT nation_key, name
    FROM (
        VALUES (1, 'Nation1'),
               (2, 'Nation2')
    ) AS Nation(nation_key, name)
),
RegionCTE AS (
    SELECT region_key, name
    FROM (
        VALUES (1, 'Region1'),
               (2, 'Region2')
    ) AS Region(region_key, name)
)
SELECT C.customer_key, N.name AS Nation_Name, R.region_key, R.name AS Region_Name
FROM CustomerCTE AS C
JOIN NationCTE AS N ON C.customer_key = N.nation_key
JOIN RegionCTE AS R ON N.nation_key = R.region_key
ORDER BY N.name, R.name