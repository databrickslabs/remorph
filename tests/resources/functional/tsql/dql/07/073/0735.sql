-- tsql sql:
CREATE SYMMETRIC KEY my_symmetric_key
WITH ALGORITHM = AES_256
ENCRYPTION BY PASSWORD = 'my_passphrase';

OPEN SYMMETRIC KEY my_symmetric_key
DECRYPTION BY PASSWORD = 'my_passphrase';

WITH patient_data AS (
    SELECT CONVERT(VARBINARY, ENCRYPTBYKEY(KEY_GUID('my_symmetric_key'), CONVERT(VARBINARY, 'Patient tested positive for COVID-19'))) AS encrypted_info
)

SELECT CONVERT(VARCHAR, DECRYPTBYKEY(encrypted_info)) AS decrypted_info
FROM patient_data;

CLOSE SYMMETRIC KEY my_symmetric_key;

-- REMORPH CLEANUP: DROP SYMMETRIC KEY my_symmetric_key;
