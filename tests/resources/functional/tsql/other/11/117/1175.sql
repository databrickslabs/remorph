-- tsql sql:
WITH DummyCTE AS (
    SELECT 1 AS DummyColumn
)
SELECT 'CREATE SYMMETRIC KEY CustomerKey123 WITH ALGORITHM = AES_256 ENCRYPTION BY CERTIFICATE CustomerCert01;' AS Query
FROM DummyCTE
UNION ALL
SELECT 'OPEN SYMMETRIC KEY CustomerKey123 DECRYPTION BY CERTIFICATE CustomerCert01 WITH PASSWORD = ''strongPassword123'';' AS Query
FROM DummyCTE
UNION ALL
SELECT 'ALTER SYMMETRIC KEY CustomerKey123 ADD ENCRYPTION BY PASSWORD = ''strongPassword123'';' AS Query
FROM DummyCTE
UNION ALL
SELECT 'ALTER SYMMETRIC KEY CustomerKey123 DROP ENCRYPTION BY CERTIFICATE CustomerCert01;' AS Query
FROM DummyCTE
UNION ALL
SELECT 'CLOSE SYMMETRIC KEY CustomerKey123;' AS Query
FROM DummyCTE