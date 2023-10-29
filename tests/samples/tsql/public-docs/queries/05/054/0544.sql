-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-scoped-credential-transact-sql?view=azuresqldb-current

ALTER DATABASE SCOPED CREDENTIAL AppCred WITH IDENTITY = 'RettigB',
    SECRET = 'sdrlk8$40-dksli87nNN8';
GO