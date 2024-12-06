-- tsql sql:
WITH KeyInfo AS (
    SELECT 'sfj5300osdVdgwdfkli7' AS key_password,
           'sd092735kjn$&adsg' AS backup_password,
           'c:\temp\AdventureWorks2022_master_key' AS backup_file
)
SELECT 'OPEN MASTER KEY DECRYPTION BY PASSWORD = ''' + key_password + ''';
       BACKUP MASTER KEY TO FILE = ''' + backup_file + '''
       ENCRYPTION BY PASSWORD = ''' + backup_password + ''';' AS sql_command
FROM KeyInfo;
