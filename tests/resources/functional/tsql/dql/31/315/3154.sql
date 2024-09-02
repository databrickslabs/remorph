--Query type: DQL
SELECT c_customerkey, c_acctbal, CONVERT(VARCHAR(12), c_acctbal, 1) AS MoneyDisplayStyle1, GETDATE() AS CurrentDate, CONVERT(VARCHAR(12), GETDATE(), 3) AS DateDisplayStyle3
FROM (
    VALUES (1, 100.0),
           (2, 200.0),
           (3, 300.0)
) AS customer (c_customerkey, c_acctbal)
WHERE CAST(c_acctbal AS VARCHAR(20)) LIKE '1%';