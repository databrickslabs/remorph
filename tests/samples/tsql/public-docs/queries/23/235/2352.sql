-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/string-split-transact-sql?view=sql-server-ver16

SELECT * FROM STRING_SPLIT('E-D-C-B-A', '-', 1) ORDER BY ordinal DESC;