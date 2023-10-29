-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/greater-than-transact-sql?view=sql-server-ver16

DECLARE @a INT = 45, @b INT = 40;  
SELECT IIF ( @a > @b, 'TRUE', 'FALSE' ) AS Result;