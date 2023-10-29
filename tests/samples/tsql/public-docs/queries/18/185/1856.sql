-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-local-variable-transact-sql?view=sql-server-ver16

DECLARE @p Point;  
SET @p=point.SetXY(23.5, 23.5);