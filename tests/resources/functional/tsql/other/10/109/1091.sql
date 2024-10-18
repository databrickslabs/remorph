--Query type: DDL
CREATE PROCEDURE dbo.customer_procedure (@customer_name VARCHAR(25))
AS
SELECT {fn OCTET_LENGTH(@customer_name)} AS customer_name_length, c_nationkey, c_acctbal
FROM (VALUES (1, 'USA', 100.0), (2, 'CANADA', 200.0), (3, 'MEXICO', 300.0)) AS customers (c_custkey, c_nationkey, c_acctbal)
WHERE CAST(c_nationkey AS VARCHAR(10)) = {fn OCTET_LENGTH(@customer_name)};