-- tsql sql:
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'mysecretpassword123!';
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'mysecretpassword123!';

WITH TempResult AS (
    SELECT 1 AS DummyValue
)
SELECT *
FROM TempResult;

CREATE ASYMMETRIC KEY MyAsymmetricKey
WITH ALGORITHM = RSA_2048;
