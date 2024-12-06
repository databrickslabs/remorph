-- tsql sql:
WITH SimulatedFileGroup AS (
    SELECT 'NewGroup2' AS FileGroupName, NULL AS FileName, NULL AS FilePath
),
SimulatedFile AS (
    SELECT 'File2' AS FileName, 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\File2.ndf' AS FilePath, 512000 AS SizeKB
)
SELECT *
FROM SimulatedFileGroup
UNION ALL
SELECT *
FROM SimulatedFile;
