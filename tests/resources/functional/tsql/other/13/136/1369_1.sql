-- tsql sql:
WITH ClassifierCTE AS (
    SELECT 'classifierC' AS ClassifierName, 'wgAdminQueries' AS WorkloadGroup, 'adminloginB' AS MemberName, 'HIGH' AS Importance, '08:00' AS StartTime, '17:00' AS EndTime
)
SELECT *
FROM ClassifierCTE;
