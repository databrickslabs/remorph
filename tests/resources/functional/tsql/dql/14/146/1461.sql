--Query type: DQL
DECLARE @EncryptThis NVARCHAR(32);
SET @EncryptThis = 'gfdsaqWE45poiuYT$%^&*()';
SELECT HASHBYTES('SHA2_256', EncryptThis) AS EncryptedValue
FROM (
    VALUES (CONVERT(NVARCHAR(32), @EncryptThis))
) AS temp(EncryptThis);