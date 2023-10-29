-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-filelistonly-transact-sql?view=sql-server-ver16

RESTORE FILELISTONLY FROM AdventureWorksBackups   
   WITH FILE=2;  
GO