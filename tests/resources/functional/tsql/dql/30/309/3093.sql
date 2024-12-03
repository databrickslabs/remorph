--Query type: DQL
SELECT CAST(ROUND(o_totalprice / o_freight, 0) AS INT) AS Computed
FROM (
    VALUES (100, 10),
           (200, 20),
           (300, 30)
) AS orders (o_totalprice, o_freight)
WHERE o_freight != 0
