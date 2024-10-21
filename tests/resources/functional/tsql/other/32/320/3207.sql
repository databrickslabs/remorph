--Query type: DCL
WITH symmetric_keys AS (
    SELECT 'NewInventoryKey' AS name,
           'AES_256' AS algorithm,
           'PassPhrase123!' AS key_source,
           'IdentityValue123!' AS identity_value
),
     database_principals AS (
    SELECT 'NewUser' AS name,
           'WITHOUT LOGIN' AS type,
           NULL AS dummy1,
           NULL AS dummy2
)
SELECT *
FROM symmetric_keys
UNION ALL
SELECT *
FROM database_principals;