-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-headeronly-transact-sql?view=sql-server-ver16

RESTORE HEADERONLY
FROM DISK = N'C:\AdventureWorks-FullBackup.bak';
GO