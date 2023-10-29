-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azuresqldb-current

SELECT LEAST('Glacier', N'Joshua Tree', 'Mount Rainier') AS LeastString;
GO