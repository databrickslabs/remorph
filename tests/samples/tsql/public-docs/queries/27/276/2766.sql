-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/string-escape-transact-sql?view=sql-server-ver16

SELECT STRING_ESCAPE('\   /  
\\    "     ', 'json') AS escapedText;