-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/try-parse-transact-sql?view=sql-server-ver16

SELECT  
    CASE WHEN TRY_PARSE('Aragorn' AS decimal USING 'sr-Latn-CS') IS NULL  
        THEN 'True'  
        ELSE 'False'  
END  
AS Result;