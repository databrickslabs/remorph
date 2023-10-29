-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-language-transact-sql?view=sql-server-ver16

ALTER EXTERNAL LANGUAGE Java 
SET (CONTENT = N'<path-to-zip>', FILE_NAME = 'javaextension.dll');
GO