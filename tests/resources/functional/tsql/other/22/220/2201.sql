--Query type: DML
INSERT INTO EncryptedData (Id, EncryptedValue)
VALUES (1, ENCRYPTBYCERT(CERT_ID('MyCertificate'), 'Data to encrypt'));
