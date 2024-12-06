-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS c (c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.0),
               (2, 1, 200.0),
               (3, 2, 50.0)
    ) AS o (o_orderkey, o_custkey, o_totalprice)
)
SELECT c.c_name,
       NTILE(4) OVER (ORDER BY SUM(o.o_totalprice) DESC) AS Quartile,
       CONVERT(VARCHAR(13), SUM(o.o_totalprice), 1) AS TotalPrice
FROM CustomerCTE c
INNER JOIN OrderCTE o
    ON c.c_custkey = o.o_custkey
WHERE o.o_orderkey IS NOT NULL AND o.o_totalprice <> 0
GROUP BY c.c_name
ORDER BY Quartile, c.c_name;
