-- tsql sql:
CREATE SYMMETRIC KEY my_symmetric_key
    WITH ALGORITHM = AES_256
    ENCRYPTION BY PASSWORD = 'password123';

OPEN SYMMETRIC KEY my_symmetric_key
    DECRYPTION BY PASSWORD = 'password123';

WITH encrypted_data AS (
    SELECT CONVERT(VARCHAR(255), ENCRYPTBYKEY(KEY_GUID('my_symmetric_key'), 'aspirin')) AS encrypted_medicine
)

SELECT CONVERT(VARCHAR(255), DECRYPTBYKEY(encrypted_medicine)) AS medicine
FROM encrypted_data;

CLOSE SYMMETRIC KEY my_symmetric_key;
