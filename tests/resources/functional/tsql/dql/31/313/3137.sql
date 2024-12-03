--Query type: DQL
SELECT TOP (10) c_customer_sk, c_current_addr_sk, c_birth_year FROM (VALUES (1, 2, 1990), (2, 3, 1991), (3, 4, 1992), (4, 5, 1993), (5, 6, 1994), (6, 7, 1995), (7, 8, 1996), (8, 9, 1997), (9, 10, 1998), (10, 11, 1999)) AS customer (c_customer_sk, c_current_addr_sk, c_birth_year);
