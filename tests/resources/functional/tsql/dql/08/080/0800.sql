--Query type: DQL
WITH binary_data AS (
    SELECT 'Hello' AS original_value,
           CAST('0x1234567890abcdef' AS VARBINARY(MAX)) AS binary_column,
           CAST('0x1234567890abcdef' AS VARBINARY(MAX)) AS encrypted_binary_column
)
SELECT original_value,
       binary_column,
       master.dbo.fn_varbintohexstr(binary_column) AS decoded,
       CONVERT(VARCHAR(MAX), DECRYPTBYKEY(encrypted_binary_column)) AS decrypted,
       master.dbo.fn_varbintohexstr(CONVERT(VARBINARY(MAX), DECRYPTBYKEY(encrypted_binary_column))) AS decrypted_and_decoded
FROM binary_data;