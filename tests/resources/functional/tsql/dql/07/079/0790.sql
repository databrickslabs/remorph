--Query type: DQL
SELECT T2.customer_name
FROM (
    VALUES ('Customer#000000001', 10.0),
           ('Customer#000000002', 20.0)
) AS T1 (customer_name, order_total)
INNER JOIN (
    VALUES ('Customer#000000001', '2020-01-01'),
           ('Customer#000000002', '2020-01-02')
) AS T2 (customer_name, order_date)
    ON T1.customer_name = T2.customer_name
ORDER BY T2.customer_name