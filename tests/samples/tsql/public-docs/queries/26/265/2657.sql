-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azuresqldb-current

SELECT LEAST('6.62', 3.1415, N'7') AS LeastVal;
GO