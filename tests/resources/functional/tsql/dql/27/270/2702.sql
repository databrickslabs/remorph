-- tsql sql:
SELECT PARSE('$' + CONVERT(VARCHAR(10), t1.extendedprice) AS DECIMAL(10, 2) USING 'en-US') AS Result FROM (VALUES (1, 10.99), (2, 20.99), (3, 30.99)) t1 (orderid, extendedprice);
