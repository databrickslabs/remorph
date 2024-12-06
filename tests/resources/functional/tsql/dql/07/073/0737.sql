-- tsql sql:
WITH temp_result AS (
    SELECT ENCRYPTBYPASSPHRASE('password123', 'aspirin') AS encrypted_medicine_name,
           'John Smith AAD' AS aad,
           'password123' AS passphrase
)
SELECT CONVERT(VARCHAR(255), DECRYPTBYPASSPHRASE(passphrase, encrypted_medicine_name)) AS decrypted_medicine
FROM temp_result
