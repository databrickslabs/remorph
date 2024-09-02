--Query type: DQL
WITH customer_region AS (
    SELECT ISNULL(c_mktsegment, 'Unknown') AS mktsegment,
           c.c_custkey
    FROM (
        VALUES ('BUILDING', 1),
               ('MACHINERY', 2),
               ('AUTOMOBILE', 3)
    ) AS c (c_mktsegment, c_custkey)
    INNER JOIN (
        VALUES (1, 'USA'),
               (2, 'Canada'),
               (3, 'Mexico')
    ) AS r (c_custkey, c_nation)
        ON c.c_custkey = r.c_custkey
    LEFT JOIN (
        VALUES ('USA', 'North America'),
               ('Canada', 'North America'),
               ('Mexico', 'North America')
    ) AS n (c_nation, c_region)
        ON r.c_nation = n.c_nation
)
SELECT TOP 1 mktsegment
FROM customer_region
WHERE c_custkey = 1
ORDER BY (CASE mktsegment WHEN 'BUILDING' THEN -1 ELSE mktsegment END) DESC;