--Query type: DDL
WITH GeneralDataCTE AS (
    SELECT 1 AS ID, 'GeneralData' AS DataField
),
SensitiveDataCTE AS (
    SELECT 1 AS ID, 'SensitiveData' AS DataField
)
SELECT *
FROM GeneralDataCTE
UNION ALL
SELECT *
FROM SensitiveDataCTE;