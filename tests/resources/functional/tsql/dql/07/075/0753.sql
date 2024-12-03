--Query type: DQL
SELECT c_name, c_acctbal, RANK() OVER (ORDER BY c_acctbal DESC) AS account_balance_rank FROM (VALUES ('Customer1', 100.00), ('Customer2', 200.00), ('Customer3', 50.00)) AS customer_data (c_name, c_acctbal);
