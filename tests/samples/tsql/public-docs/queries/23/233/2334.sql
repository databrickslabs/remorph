-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/collation-precedence-transact-sql?view=sql-server-ver16

SELECT *   
FROM TestTab   
WHERE GreekCol = LatinCol;