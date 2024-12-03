--Query type: DQL
SELECT c_customer_sk, c_first_name, c_birth_date FROM (VALUES (1, 'John', '1990-01-01'), (2, 'Mary', '1995-06-15')) AS customers (c_customer_sk, c_first_name, c_birth_date) ORDER BY DATEPART(year, c_birth_date);
