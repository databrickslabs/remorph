--Query type: DML
WITH BackupSimulation AS (
    SELECT 'MarketingGroup1' AS FileGroup, 'Z:\SQLServerBackups\MarketingFiles.bck' AS BackupFile
    UNION ALL
    SELECT 'MarketingGroup2', 'Z:\SQLServerBackups\MarketingFiles.bck'
)
SELECT *
FROM BackupSimulation;
