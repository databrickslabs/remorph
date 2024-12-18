-- tsql sql:
SELECT * FROM (VALUES ('2017-12-31', 100.00), ('2018-01-15', 200.00), ('2017-11-20', 50.00)) AS orders (order_date, total_amount) WHERE order_date < '2018-01-01';
