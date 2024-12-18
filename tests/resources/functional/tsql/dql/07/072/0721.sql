-- tsql sql:
CREATE SYMMETRIC KEY MySymmetricKey
WITH ALGORITHM = AES_256
ENCRYPTION BY PASSWORD = 'password123';

OPEN SYMMETRIC KEY MySymmetricKey
DECRYPTION BY PASSWORD = 'password123';

WITH encrypted_data AS (
    SELECT CONVERT(VARCHAR(256), ENCRYPTBYKEY(KEY_GUID('MySymmetricKey'), 'antibiotics')) AS encrypted_medicine
)

SELECT CONVERT(VARCHAR(256), DECRYPTBYKEY(encrypted_medicine)) AS decrypted_medicine
FROM encrypted_data;

CLOSE SYMMETRIC KEY MySymmetricKey;

DROP SYMMETRIC KEY MySymmetricKey;
