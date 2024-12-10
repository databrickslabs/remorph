-- tsql sql:
WITH GeneralDataCTE AS (
    SELECT 1 AS ID, 'General Data' AS DataField
),
SensitiveDataCTE AS (
    SELECT 2 AS ID, 'Sensitive Data' AS DataField
)
SELECT ID, DataField
FROM GeneralDataCTE
UNION ALL
SELECT ID, DataField
FROM SensitiveDataCTE
