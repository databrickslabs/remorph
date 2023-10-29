-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/ltrim-transact-sql?view=sql-server-ver16

DECLARE @string_to_trim VARCHAR(60);  
SET @string_to_trim = '     Five spaces are at the beginning of this string.';  
SELECT  
    @string_to_trim AS 'Original string',
    LTRIM(@string_to_trim) AS 'Without spaces';  
GO