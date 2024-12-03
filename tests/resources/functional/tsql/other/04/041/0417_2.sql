--Query type: DML
CREATE ASYMMETRIC KEY Employee_AKey
WITH ALGORITHM = RSA_2048;

CREATE SYMMETRIC KEY Employee_Key_01
WITH ALGORITHM = AES_256
ENCRYPTION BY ASYMMETRIC KEY Employee_AKey;

OPEN SYMMETRIC KEY Employee_Key_01
DECRYPTION BY ASYMMETRIC KEY Employee_AKey;

WITH Employee_Data AS (
    SELECT 1 AS EmployeeID,
           ENCRYPTBYKEY(KEY_GUID('Employee_Key_01'), CONVERT(varchar, 1)) AS EncryptedEmployeeID
    UNION ALL
    SELECT 2 AS EmployeeID,
           ENCRYPTBYKEY(KEY_GUID('Employee_Key_01'), CONVERT(varchar, 2)) AS EncryptedEmployeeID
    UNION ALL
    SELECT 3 AS EmployeeID,
           ENCRYPTBYKEY(KEY_GUID('Employee_Key_01'), CONVERT(varchar, 3)) AS EncryptedEmployeeID
)
SELECT EmployeeID,
       EncryptedEmployeeID AS 'Encrypted Employee ID',
       CONVERT(nvarchar, DECRYPTBYKEY(EncryptedEmployeeID)) AS 'Decrypted Employee ID'
FROM Employee_Data;

CLOSE SYMMETRIC KEY Employee_Key_01;

-- REMORPH CLEANUP: DROP SYMMETRIC KEY Employee_Key_01;
-- REMORPH CLEANUP: DROP ASYMMETRIC KEY Employee_AKey;
