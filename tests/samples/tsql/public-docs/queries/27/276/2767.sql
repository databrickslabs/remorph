-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/stuff-transact-sql?view=sql-server-ver16

SELECT STUFF('abcdef', 2, 3, 'ijklmn');
GO