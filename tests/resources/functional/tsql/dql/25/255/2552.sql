--Query type: DQL
SELECT DATE_BUCKET(WEEK, 1, CAST(o_orderdate AS DATETIME2)) AS OrderDateBucket,
       SUM(l_quantity) AS SumLineQuantity,
       SUM(l_extendedprice) AS SumLineExtendedPrice
FROM (
    VALUES ('1992-01-01', 10, 100.0),
           ('1992-01-08', 20, 200.0),
           ('1992-01-15', 30, 300.0)
) AS Orders(o_orderdate, l_quantity, l_extendedprice)
WHERE o_orderdate BETWEEN '1992-01-01 00:00:00.000' AND '1992-01-31 00:00:00.000'
GROUP BY DATE_BUCKET(WEEK, 1, CAST(o_orderdate AS DATETIME2))
ORDER BY OrderDateBucket;