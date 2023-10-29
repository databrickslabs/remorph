-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql?view=sql-server-ver16

RESTORE DATABASE AdventureWorks2022
    FROM AdventureWorksBackups
    WITH FILE = 3, NORECOVERY;

RESTORE LOG AdventureWorks2022
    FROM AdventureWorksBackups
    WITH FILE = 4, NORECOVERY, STOPAT = 'Apr 15, 2020 12:00 AM';

RESTORE LOG AdventureWorks2022
    FROM AdventureWorksBackups
    WITH FILE = 5, NORECOVERY, STOPAT = 'Apr 15, 2020 12:00 AM';
RESTORE DATABASE AdventureWorks2022 WITH RECOVERY;