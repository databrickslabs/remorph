-- tsql sql:
WITH AvailabilityGroupCTE AS (
    SELECT 'MyAvailabilityGroup' AS AvailabilityGroupName
),
DatabaseCTE AS (
    SELECT 'MyDatabase' AS DatabaseName
),
DatabaseAvailabilityGroupCTE AS (
    SELECT d.DatabaseName, ag.AvailabilityGroupName
    FROM DatabaseCTE d
    CROSS JOIN AvailabilityGroupCTE ag
)
SELECT *
FROM DatabaseAvailabilityGroupCTE;
-- REMORPH CLEANUP: No objects were created in this query.
