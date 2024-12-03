--Query type: DQL
WITH SignedData AS (
    SELECT 'data signed by certificate ''Shipping04''' AS Description,
           Cert_Id('Shipping04') AS CertId,
           'signed data' AS Data,
           CONVERT(varbinary, 'signature', 2) AS DataSignature
)
SELECT Data
FROM SignedData
WHERE VerifySignedByCert(CertId, Data, DataSignature) = 1
      AND Description = N'data signed by certificate ''Shipping04'''
