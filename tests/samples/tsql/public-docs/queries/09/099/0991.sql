-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-language-transact-sql?view=sql-server-ver16

CREATE EXTERNAL LANGUAGE Java 
FROM (CONTENT = N'<path-to-zip>', FILE_NAME = 'javaextension.dll');
GO