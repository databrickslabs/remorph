--Query type: DDL
CREATE CERTIFICATE Shipping04 ENCRYPTION BY PASSWORD = 'pGFD4bb925DGvbd2439587y' WITH SUBJECT = 'Sammamish Shipping Records', EXPIRY_DATE = '20401031';
WITH temp_result AS (
    SELECT 1 AS c_custkey, 'Customer1' AS c_name
    UNION ALL
    SELECT 2, 'Customer2'
)
SELECT * FROM temp_result;
SELECT * FROM (
    VALUES (1, 'Customer1'), (2, 'Customer2')
) AS temp_result(c_custkey, c_name);
-- REMORPH CLEANUP: DROP CERTIFICATE Shipping04;