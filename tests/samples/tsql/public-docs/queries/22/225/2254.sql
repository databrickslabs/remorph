-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

RESTORE DATABASE AdventureWorks2022
    FROM AdventureWorksBackups
    WITH NORECOVERY,
      MOVE 'AdventureWorks2022_Data' TO
'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\NewAdvWorks.mdf',
      MOVE 'AdventureWorks2022_Log'
TO 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\NewAdvWorks.ldf';
RESTORE LOG AdventureWorks2022
    FROM AdventureWorksBackups
    WITH RECOVERY;