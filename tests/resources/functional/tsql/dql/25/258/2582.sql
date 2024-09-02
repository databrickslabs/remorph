--Query type: DQL
WITH SignedDataCTE AS (
    SELECT 'data signed by certificate ''Shipping04''' AS Description,
           'signed data' AS Signed_Data,
           CONVERT(VARBINARY, 'data signature', 2) AS DataSignature,
           'data' AS Data
)
SELECT Data,
       VerifySignedByCert(Cert_Id('Customer01'), Signed_Data, DataSignature) AS IsSignatureValid
FROM SignedDataCTE
WHERE Description = N'data signed by certificate ''Customer01''';