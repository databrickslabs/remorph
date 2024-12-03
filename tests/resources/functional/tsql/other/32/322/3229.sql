--Query type: DML
CREATE TABLE #EncryptedData
(
    ID INT,
    EncryptedValue VARBINARY(MAX)
);

DECLARE @Passphrase NVARCHAR(128);

SET @Passphrase = 'A little learning is a dangerous thing!';

INSERT INTO #EncryptedData (ID, EncryptedValue)
VALUES
    (1, EncryptByPassPhrase(@Passphrase, '123-45-678', 1, CONVERT(varbinary, 1))),
    (2, EncryptByPassPhrase(@Passphrase, '987-65-432', 1, CONVERT(varbinary, 2)));

UPDATE #EncryptedData
SET EncryptedValue = EncryptByPassPhrase(@Passphrase, '111-11-111', 1, CONVERT(varbinary, ID))
WHERE ID = 1;

SELECT * FROM #EncryptedData;

-- Clean up
-- REMORPH CLEANUP: DROP TABLE #EncryptedData;
