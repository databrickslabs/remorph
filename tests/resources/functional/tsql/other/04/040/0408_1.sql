--Query type: DDL
WITH CTE_DatabaseFiles AS (
    SELECT 'TPC_H_FILE' AS FileName,
           'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\TPC_H_FILE.ndf' AS FilePath,
           5 * 1024 * 1024 AS FileSize,
           'UNLIMITED' AS MaxSize,
           '5MB' AS FileGrowth,
           'TPC_H_FG' AS FileGroupName
)
SELECT *
FROM CTE_DatabaseFiles;
