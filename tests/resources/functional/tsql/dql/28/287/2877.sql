--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_nationkey
    FROM (
        VALUES (1, 1), (2, 2), (3, 3)
    ) AS Customer(c_custkey, c_nationkey)
),
NationCTE AS (
    SELECT n_nationkey, n_name
    FROM (
        VALUES (1, 'USA'), (2, 'Canada'), (3, 'Mexico')
    ) AS Nation(n_nationkey, n_name)
)
SELECT c.c_custkey
FROM CustomerCTE c
JOIN NationCTE n ON c.c_nationkey = n.n_nationkey
WHERE n.n_name = 'USA';