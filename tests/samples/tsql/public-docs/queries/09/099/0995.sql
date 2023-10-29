-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-external-library-transact-sql?view=sql-server-ver16

CREATE EXTERNAL LIBRARY customPackage 
FROM (CONTENT = 'C:\temp\customPackage_v1.1.zip')
WITH (LANGUAGE = 'R');
GO