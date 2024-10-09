--Query type: DML
CREATE TABLE #CustomerData
(
    CustomerID INT,
    CreditCardNumber VARBINARY(128),
    EncryptedCreditCardNumber2 VARBINARY(128)
);

INSERT INTO #CustomerData (CustomerID, CreditCardNumber)
VALUES
    (1, 0x1234567890),
    (2, 0x2345678901);

OPEN SYMMETRIC KEY Customer_Key_02
DECRYPTION BY ASYMMETRIC KEY Customer_AKey;

UPDATE #CustomerData
SET EncryptedCreditCardNumber2 = EncryptByKey(Key_GUID('Customer_Key_02'), CreditCardNumber);

SELECT *
FROM #CustomerData;

-- REMORPH CLEANUP: DROP TABLE #CustomerData;
-- REMORPH CLEANUP: CLOSE SYMMETRIC KEY Customer_Key_02;