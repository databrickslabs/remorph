--Query type: DQL
SELECT TOP (1) DATEPART(year, '1994-03-21') AS order_year FROM (VALUES ('1994-03-21')) AS orders (order_date);
