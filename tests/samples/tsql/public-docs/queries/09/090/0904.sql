-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql?view=sql-server-ver16

CREATE CREDENTIAL ServiceIdentity WITH IDENTITY = 'Managed Identity';
GO