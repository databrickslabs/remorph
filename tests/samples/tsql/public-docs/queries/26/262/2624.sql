-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-greatest-transact-sql?view=azuresqldb-current

SELECT GREATEST('Glacier', N'Joshua Tree', 'Mount Rainier') AS GreatestString;
GO