--Query type: DCL
WITH TriggerStatus AS (
    SELECT 'Disabled' AS Status, 'Trigger1' AS TriggerName
    UNION ALL
    SELECT 'Enabled' AS Status, 'Trigger2' AS TriggerName
)
SELECT
    CASE
        WHEN Status = 'Disabled' THEN 'DISABLE Trigger ' + TriggerName + ' ON ALL SERVER;'
        ELSE 'ENABLE Trigger ' + TriggerName + ' ON ALL SERVER;'
    END AS TriggerCommand
FROM TriggerStatus;
