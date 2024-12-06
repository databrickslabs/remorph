-- tsql sql:
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'tpch1234567890abcdef';
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'tpch1234567890abcdef';
CREATE CERTIFICATE Customer037 WITH SUBJECT = 'Customer Service', EXPIRY_DATE = '12/31/2025';
CREATE SYMMETRIC KEY Customer_Key_01 WITH ALGORITHM = AES_256 ENCRYPTION BY CERTIFICATE Customer037;
WITH DummyCTE AS (
    SELECT 1 AS DummyColumn
)
SELECT * FROM DummyCTE;
-- REMORPH CLEANUP: DROP SYMMETRIC KEY Customer_Key_01;
-- REMORPH CLEANUP: DROP CERTIFICATE Customer037;
-- REMORPH CLEANUP: CLOSE MASTER KEY;
-- REMORPH CLEANUP: DROP MASTER KEY;
