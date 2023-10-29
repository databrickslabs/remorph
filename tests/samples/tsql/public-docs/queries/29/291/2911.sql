-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/user-name-transact-sql?view=sql-server-ver16

SELECT name FROM sysusers WHERE name = USER_NAME(1);