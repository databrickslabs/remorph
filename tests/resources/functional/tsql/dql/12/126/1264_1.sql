--Query type: DQL
SELECT c_customer_sk, c_last_name, c_first_name, ss_sales_price, ss_net_profit FROM (VALUES (1, 'Smith', 'John', 100.00, 20.00), (2, 'Johnson', 'Mary', 200.00, 30.00)) AS CustomerSales (c_customer_sk, c_last_name, c_first_name, ss_sales_price, ss_net_profit);
