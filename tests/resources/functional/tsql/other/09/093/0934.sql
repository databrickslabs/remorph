-- tsql sql:
CREATE DATABASE TestEncryption;
CREATE CERTIFICATE cert_encryption_demo ENCRYPTION BY PASSWORD = '4bb925DGvbd2439587yT'
    WITH SUBJECT = 'ENCRYPTION demo';

WITH encryption_demo AS (
    SELECT 'ENCRYPTION demo' AS subject
)
SELECT *
FROM encryption_demo;

-- REMORPH CLEANUP:
DROP DATABASE TestEncryption;
DROP CERTIFICATE cert_encryption_demo;
