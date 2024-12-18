-- tsql sql:
WITH cte AS (SELECT 'Customer01' AS cert_name)
SELECT CERTENCODED(CERT_ID(cert_name))
FROM cte
