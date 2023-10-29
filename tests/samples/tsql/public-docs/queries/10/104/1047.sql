-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-role-transact-sql?view=sql-server-ver16

CREATE LOGIN sqllogin_nlastname WITH password='aah3%#om1os';
    
 CREATE USER sqllogin_nlastname FOR LOGIN sqllogin_nlastname 
 WITH DEFAULT_SCHEMA = master;
    
 ALTER ROLE [dbmanager] add member sqllogin_nlastname;