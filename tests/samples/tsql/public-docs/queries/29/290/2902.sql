-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/wildcard-match-one-character-transact-sql?view=sql-server-ver16

SELECT name FROM sys.database_principals
WHERE name LIKE 'db_%';