-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

BACKUP DATABASE AdventureWorks2022
    TO AdventureWorksBackups ;

RESTORE FILELISTONLY
    FROM AdventureWorksBackups ;

RESTORE DATABASE TestDB
    FROM AdventureWorksBackups
    WITH MOVE 'AdventureWorks2022_Data' TO 'C:\MySQLServer\testdb.mdf',
    MOVE 'AdventureWorks2022_Log' TO 'C:\MySQLServer\testdb.ldf';
GO