--Query type: DQL
WITH EmployeeCTE AS (
    SELECT
        BusinessEntityID,
        NationalIDNumber,
        CONVERT(nvarchar, DecryptByKeyAutoCert(cert_ID('Sales037'), NULL, EncryptedNationalIDNumber)) AS 'Decrypted ID Number'
    FROM
        (
            VALUES
                (1, '123-45-6789', 'encrypted_value1'),
                (2, '987-65-4321', 'encrypted_value2')
        ) AS Employee(BusinessEntityID, NationalIDNumber, EncryptedNationalIDNumber)
)
SELECT
    BusinessEntityID,
    NationalIDNumber,
    'Encrypted ID Number' AS 'Encrypted ID Number',
    'Decrypted ID Number' AS 'Decrypted ID Number'
FROM
    EmployeeCTE
