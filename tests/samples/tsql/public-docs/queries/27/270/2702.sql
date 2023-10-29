-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/parse-transact-sql?view=sql-server-ver16

SELECT PARSE('&euro;345,98' AS money USING 'de-DE') AS Result;