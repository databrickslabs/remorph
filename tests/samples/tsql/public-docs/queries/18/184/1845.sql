-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-type-conversion-database-engine?view=sql-server-ver16

DECLARE @notastring INT;
SET @notastring = '1';
SELECT @notastring + '1'