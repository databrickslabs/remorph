--Query type: DCL
SET CONCAT_NULL_YIELDS_NULL ON;

WITH CustomerCTE AS (
    SELECT 'Customer#1' AS C_NAME, 'United States' AS C_NATIONKEY, 100.00 AS C_ACCTBAL
),
NationCTE AS (
    SELECT 'United States' AS N_NAME, 1 AS N_NATIONKEY
)

SELECT 'Customer from ' + C.C_NAME + ' in ' + N.N_NAME + ' has ' + CONVERT(VARCHAR, C.C_ACCTBAL) + ' balance' AS ResultWhen_ON,
       @@OPTIONS AS OptionsValueWhen_ON
FROM CustomerCTE C
INNER JOIN NationCTE N ON C.C_NATIONKEY = N.N_NATIONKEY
