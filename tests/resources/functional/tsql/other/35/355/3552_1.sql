--Query type: DDL
CREATE CERTIFICATE TPC_H_CERT
WITH SUBJECT = 'TPC_H_CERTIFICATE';

WITH DataToEncrypt AS (
  SELECT TOP 10 o_orderkey, o_custkey
  FROM (
    VALUES (1, 1000), (2, 1001), (3, 1002), (4, 1003), (5, 1004),
           (6, 1005), (7, 1006), (8, 1007), (9, 1008), (10, 1009)
  ) AS Orders(o_orderkey, o_custkey)
)
SELECT 
  o_orderkey,
  o_custkey,
  ENCRYPTBYKEY(KEY_GUID('TPC_H_CERT'), CONVERT(varchar, o_custkey)) AS Encrypted_custkey
INTO #EncryptedData
FROM DataToEncrypt;

SELECT * FROM #EncryptedData;
-- REMORPH CLEANUP: DROP TABLE #EncryptedData;
-- REMORPH CLEANUP: DROP CERTIFICATE TPC_H_CERT;