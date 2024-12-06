-- tsql sql:
WITH RestoreFiles AS (
    SELECT 'customer_data_1' AS FileName, 'new_orders' AS FileGroup, 9 AS FileNumber
    UNION ALL
    SELECT 'customer_data_2', 'new_orders', 10
)
SELECT 'RESTORE DATABASE TPC_H_DB FILE = ''' + FileName + ''', FILEGROUP = ''' + FileGroup + ''' FROM DISK = ''path_to_backup_file'' WITH FILE = ' + CONVERT(VARCHAR, FileNumber) + ', NORECOVERY;' AS RestoreCommand
FROM RestoreFiles;
