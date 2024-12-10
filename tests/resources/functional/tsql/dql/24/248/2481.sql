-- tsql sql:
SELECT CONVERT(CHAR(8), c_customer_sk, 112) AS customer_style, CONVERT(CHAR(8), c_nationkey, 112) AS nation_style, CONVERT(CHAR(8), c_acctbal, 112) AS account_style FROM (VALUES (1, 5, 100.00), (2, 10, 200.00), (3, 15, 300.00)) AS customer_data (c_customer_sk, c_nationkey, c_acctbal);
