--Query type: DCL
WITH DeniedPermissions AS (
    SELECT 'Mirror7' AS EndpointName, 'VIEW DEFINITION' AS Permission
)
SELECT 'DENY ' + Permission + ' ON ENDPOINT::' + EndpointName AS SimulatedQuery
FROM DeniedPermissions;