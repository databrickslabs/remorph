-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver16

SELECT TRIM(TRAILING '.,! ' FROM '     .#     test    .') AS Result;