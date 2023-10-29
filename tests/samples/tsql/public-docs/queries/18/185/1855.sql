-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-local-variable-transact-sql?view=sql-server-ver16

DECLARE @p Point;  
SET @p.X = @p.X + 1.1;  
SELECT @p;  
GO