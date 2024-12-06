-- tsql sql:
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'new_password';

DECLARE @KeyName sysname = 'NewKey';

CREATE ASYMMETRIC KEY NewKey WITH ALGORITHM = RSA_2048;

OPEN MASTER KEY DECRYPTION BY PASSWORD = 'new_password';

ALTER ASYMMETRIC KEY [NewKey] WITH PRIVATE KEY (DECRYPTION BY PASSWORD = 'new_password');

SELECT @KeyName AS KeyName FROM (VALUES (1)) AS temp (Column1);

-- REMORPH CLEANUP: DROP ASYMMETRIC KEY NewKey;
-- REMORPH CLEANUP: DROP MASTER KEY;
