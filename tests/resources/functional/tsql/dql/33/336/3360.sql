-- tsql sql:
SELECT p_name, p_retailprice FROM (VALUES ('Mountain Bike', 80.99), ('Road Bike', 100.99)) AS products (p_name, p_retailprice) WHERE p_retailprice = 80.99 AND p_name LIKE '%Mountain%';