-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver16

SELECT TRIM(LEADING '.,! ' FROM  '     .#     test    .') AS Result;