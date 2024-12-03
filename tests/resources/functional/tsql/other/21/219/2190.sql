--Query type: DML
DECLARE @cleartext nvarchar(100) = 'This is some clear text';
CREATE ASYMMETRIC KEY MyAsymKey WITH ALGORITHM = RSA_2048;
CREATE TABLE Sales.ProtectedData (
    EncryptedData varbinary(max)
);
IF NOT EXISTS (
    SELECT *
    FROM sys.tables
    WHERE name = 'ProtectedData'
    AND schema_id = SCHEMA_ID('Sales')
)
CREATE TABLE Sales.ProtectedData (
    EncryptedData varbinary(max)
);
INSERT INTO Sales.ProtectedData (
    EncryptedData
)
VALUES (
    (
        SELECT EncryptByAsymKey(AsymKey_ID('MyAsymKey'), @cleartext) AS EncryptedData
    )
);
SELECT *
FROM Sales.ProtectedData;
-- REMORPH CLEANUP: DROP TABLE Sales.ProtectedData;
-- REMORPH CLEANUP: DROP ASYMMETRIC KEY MyAsymKey;
