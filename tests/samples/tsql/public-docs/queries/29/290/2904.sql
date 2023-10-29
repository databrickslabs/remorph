-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/wildcard-character-s-to-match-transact-sql?view=sql-server-ver16

SELECT name FROM sys.databases
WHERE name LIKE 'm[n-z]%';