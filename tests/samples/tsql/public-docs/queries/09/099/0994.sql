-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql?view=sql-server-ver16

CREATE EXTERNAL LIBRARY customPackage
FROM (CONTENT = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\customPackage.zip') WITH (LANGUAGE = 'R');