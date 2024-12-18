-- tsql sql:
WITH customer_info AS (SELECT 'Customer#000000001' AS name, 10 AS custkey),
    supplier_info AS (SELECT 'Supplier#000000001' AS name, 10 AS suppkey)
SELECT c.name + '.' + s.name AS [Customer and supplier names]
FROM customer_info AS c
JOIN supplier_info AS s
    ON c.custkey = s.suppkey;
