-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql?view=sql-server-ver16

CREATE EXTERNAL LIBRARY packageA 
FROM (CONTENT = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\packageA.zip') 
WITH (LANGUAGE = 'R'); 
GO

CREATE EXTERNAL LIBRARY packageB FROM (CONTENT = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\packageB.zip') 
WITH (LANGUAGE = 'R');
GO

CREATE EXTERNAL LIBRARY packageC FROM (CONTENT = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\packageC.zip') 
WITH (LANGUAGE = 'R');
GO