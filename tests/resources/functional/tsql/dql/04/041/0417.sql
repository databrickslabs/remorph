--Query type: DQL
WITH EmployeeCTE AS (
    SELECT BusinessEntityID, NationalIDNumber, EncryptedNationalIDNumber2
    FROM (
        VALUES (1, '123456789', 'encrypted_value1'),
               (2, '987654321', 'encrypted_value2')
    ) AS Employee(BusinessEntityID, NationalIDNumber, EncryptedNationalIDNumber2)
)
SELECT BusinessEntityID, EncryptedNationalIDNumber2 AS [Encrypted ID Number],
       CONVERT(nvarchar, DecryptByKeyAutoAsymKey(AsymKey_ID('Customer_AKey'), NULL, EncryptedNationalIDNumber2)) AS [Decrypted ID Number]
FROM EmployeeCTE;