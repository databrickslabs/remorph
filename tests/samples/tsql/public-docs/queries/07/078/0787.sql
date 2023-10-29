-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql?view=sql-server-ver16

BACKUP DATABASE Sales
TO      URL = 's3://10.10.10.10:8787/sqls3backups/sales_01.bak'
,       URL = 's3://10.10.10.10:8787/sqls3backups/sales_02.bak'
,       URL = 's3://10.10.10.10:8787/sqls3backups/sales_03.bak'
WITH    FORMAT
,       STATS               = 10
,       COMPRESSION;