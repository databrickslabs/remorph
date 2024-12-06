-- tsql sql:
SELECT DISTINCT
    DATE_BUCKET(DAY, 30, CAST(o_orderdate AS DATETIME2)) AS DateBucket,
    FIRST_VALUE(o_orderkey) OVER (
        ORDER BY DATE_BUCKET(DAY, 30, CAST(o_orderdate AS DATETIME2))
    ) AS First_Value_In_Bucket,
    LAST_VALUE(o_orderkey) OVER (
        ORDER BY DATE_BUCKET(DAY, 30, CAST(o_orderdate AS DATETIME2))
    ) AS Last_Value_In_Bucket
FROM (
    VALUES
        ('1992-01-01', 1), ('1992-01-02', 2), ('1992-01-03', 3), ('1992-01-04', 4), ('1992-01-05', 5),
        ('1992-01-06', 6), ('1992-01-07', 7), ('1992-01-08', 8), ('1992-01-09', 9), ('1992-01-10', 10)
) AS orders (o_orderdate, o_orderkey)
WHERE o_orderdate BETWEEN '1992-01-01 00:00:00.000' AND '1992-01-31 00:00:00.000'
ORDER BY DateBucket;
