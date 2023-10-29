-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-library-transact-sql?view=sql-server-ver16

ALTER EXTERNAL LIBRARY customPackage 
SET 
  (CONTENT = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\customPackage.zip')
WITH (LANGUAGE = 'R');